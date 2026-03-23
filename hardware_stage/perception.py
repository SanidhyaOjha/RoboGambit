import math
import cv2
import cv2.aruco as aruco
import numpy as np
import socket
import struct

# ── Socket config ─────────────────────────────────────────────────────────────
SERVER_IP   = '10.168.70.199' #update this to server's IP address
SERVER_PORT = 9999

# ── Camera intrinsics ─────────────────────────────────────────────────────────
CAMERA_MATRIX = np.array([
    [1030.4890823364258, 0,   960],
    [0, 1030.489103794098, 540],
    [0,                0,   1]
], dtype=np.float32)
DIST_COEFFS = np.zeros((1, 5), dtype=np.float32)

# ── Board geometry ────────────────────────────────────────────────────────────
CORNER_WORLD = {
    21: (350,  350),
    22: (350, -350),
    23: (-350, -350),
    24: (-350,  350),
}
SQUARE_SIZE = 100
TOP_LEFT_X  = 300
TOP_LEFT_Y  = 300
BOARD_SIZE  = 6
PIECE_IDS   = set(range(1, 11))

# ── ArUco setup ───────────────────────────────────────────────────────────────
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
params     = aruco.DetectorParameters()
params.cornerRefinementMethod      = aruco.CORNER_REFINE_SUBPIX
params.adaptiveThreshWinSizeMin    = 3
params.adaptiveThreshWinSizeMax    = 35
params.adaptiveThreshWinSizeStep   = 10
params.minMarkerPerimeterRate      = 0.03
params.maxMarkerPerimeterRate      = 4.0
params.polygonalApproxAccuracyRate = 0.03
params.minCornerDistanceRate       = 0.05
params.minDistanceToBorder         = 1
detector = aruco.ArucoDetector(aruco_dict, params)

# ── State ─────────────────────────────────────────────────────────────────────
H_matrix      = None
corner_pixels = {}
prev_board    = None


# ── Helpers ───────────────────────────────────────────────────────────────────
def pixel_to_world(H, px, py):
    pt = cv2.perspectiveTransform(
        np.array([[[px, py]]], dtype=np.float32), H
    )
    return float(pt[0][0][0]), float(pt[0][0][1])


def world_to_cell(wx, wy):
    best_row, best_col, min_dist = None, None, float('inf')
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            cx = TOP_LEFT_X - (row * SQUARE_SIZE + SQUARE_SIZE / 2)
            cy = TOP_LEFT_Y - (col * SQUARE_SIZE + SQUARE_SIZE / 2)
            d  = math.hypot(wx - cx, wy - cy)
            if d < min_dist:
                min_dist, best_row, best_col = d, row, col
    return best_row, best_col


def build_board(ids, corners, H):
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    for i, mid in enumerate(ids.flatten()):
        if mid not in PIECE_IDS:
            continue
        c  = corners[i][0]
        px = float(np.mean(c[:, 0]))
        py = float(np.mean(c[:, 1]))
        wx, wy   = pixel_to_world(H, px, py)
        row, col = world_to_cell(wx, wy)
        if row is not None:
            board[row][col] = mid
    return board


def recv_frame(sock, data, payload_size):
    """Read one frame from the socket stream. Returns (frame, data_remainder)."""
    # Read header
    while len(data) < payload_size:
        packet = sock.recv(4096)
        if not packet:
            return None, data
        data += packet

    packed_msg_size = data[:payload_size]
    data            = data[payload_size:]
    msg_size        = struct.unpack("Q", packed_msg_size)[0]

    # Read frame bytes
    while len(data) < msg_size:
        packet = sock.recv(4096)
        if not packet:
            return None, data
        data += packet

    frame_data = data[:msg_size]
    data       = data[msg_size:]

    frame = cv2.imdecode(
        np.frombuffer(frame_data, dtype=np.uint8),
        cv2.IMREAD_COLOR
    )
    return frame, data


# ── Connect ───────────────────────────────────────────────────────────────────
print(f"Connecting to {SERVER_IP}:{SERVER_PORT} ...")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
print("Connected ✓")

payload_size = struct.calcsize("Q")
data_buffer  = b""

# ── Main loop ─────────────────────────────────────────────────────────────────
try:
    while True:
        frame, data_buffer = recv_frame(client_socket, data_buffer, payload_size)
        if frame is None:
            print("Stream ended or connection lost.")
            break

        frame        = cv2.undistort(frame, CAMERA_MATRIX, DIST_COEFFS, None, CAMERA_MATRIX)
        gray         = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = detector.detectMarkers(gray)

        board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

        if ids is not None:

            # Update corner pixels every frame
            for i, mid in enumerate(ids.flatten()):
                if mid in CORNER_WORLD:
                    corner_pixels[mid] = np.mean(corners[i][0], axis=0)

            # Lock homography once all 4 corners seen
            if H_matrix is None and len(corner_pixels) == 4:
                pixel_pts = np.array([corner_pixels[m] for m in [21, 22, 23, 24]], dtype=np.float32)
                world_pts = np.array([CORNER_WORLD[m]  for m in [21, 22, 23, 24]], dtype=np.float32)
                H_matrix, _ = cv2.findHomography(pixel_pts, world_pts)
                print("Homography locked ✓")

            # Build board state
            if H_matrix is not None:
                board = build_board(ids, corners, H_matrix)

        # Print only when board changes
        if prev_board is None or not np.array_equal(board, prev_board):
            print("\nBoard state:\n", board)
            prev_board = board.copy()

        cv2.imshow("ArUco Detection", frame)
        if cv2.waitKey(1) & 0xFF == 27:   # ESC to quit
            break

except KeyboardInterrupt:
    print("\nInterrupted.")

finally:
    client_socket.close()
    cv2.destroyAllWindows()
    print("Disconnected.")