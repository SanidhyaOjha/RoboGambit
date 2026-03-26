import game
import numpy as np
import requests
import argparse
import serial
import time
from perception import board


BOARD = np.zeros((6, 6), dtype=int)
# Serial port for the arm
ser = serial.Serial("COM4", baudrate=115200, dsrdtr=None)
ser.setRTS(False)
ser.setDTR(False)
# Serial port for the Solenoid
ser2 = serial.Serial('COM3', 115200) 

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
    ser2.write(b'1')

def place():
    """Send the command to place a piece."""
    ser2.write(b'0')

def send_cmd(command: str):
    """Send the move string to the robot's actuators."""
     # add code to send move_str to the robot
    print(f"Sending command: {command}")
    ser.write(command.encode() + b'\n')

if __name__ == "__main__":
    # write code to run the main loop of the program, calling move() and send_cmd() as needed
    pass

