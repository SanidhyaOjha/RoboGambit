import game
import numpy as np
import requests
import argparse
import serial
import time
from perception import board

ser = serial.Serial('COM3', 115200) 
BOARD = np.zeros((6, 6), dtype=int)

def get_board_state() -> np.ndarray:
    """Use the perception module to get the current board state."""
    # add code to update BOARD using perception.board
    return BOARD

def move() -> str:
    """Determine the best move using the game module."""
    return game.get_best_move(get_board_state(board))

def movetocmd(move:str) -> str:
    """convert the move string to a command string for the robot."""
    pass

def pick():
    """Send the command to pick up a piece."""
    ser.write(b'1')

def place():
    """Send the command to place a piece."""
    ser.write(b'0')

def send_cmd(command: str):
    """Send the move string to the robot's actuators."""
    print(f"Sending command: {command}")
    parser = argparse.ArgumentParser(description='Http JSON Communication')
    

    args = parser.parse_args()

    ip_addr = "192.168.4.1"

    try:
        while True:
            
            url = "http://" + ip_addr + "/js?json=" + command
            response = requests.get(url)
            content = response.text
            print(content)
    except KeyboardInterrupt:
        pass
    # add code to send move_str to the robot

if __name__ == "__main__":
    # write code to run the main loop of the program, calling move() and send_cmd() as needed
    pass

