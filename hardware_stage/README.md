# Hardware Stage

This folder contains the implementation for the Hardware Stage of RoboGambit, where the simulated system is deployed on physical robotic hardware.

## Overview

The Hardware Stage involves controlling two 4-DOF robotic arms to play a chess-inspired mini-game on a 6x6 board. The system integrates:

- **Perception**: Computer vision using ArUco markers to detect board state
- **Game Logic**: AI algorithm to determine optimal moves
- **Robotic Control**: Serial and HTTP communication with the robotic arms

## Files

- `main.py`: Main control script that orchestrates perception, game logic, and robot commands
- `game.py`: Game AI implementation (currently a placeholder - implement your game logic here)
- `perception.py`: Computer vision module for board state detection using ArUco markers

## Setup

### Dependencies

Install required Python packages:

```bash
pip install numpy opencv-python requests pyserial 
```

### Hardware Requirements

- Two 4-DOF robotic arms with serial communication
- Overhead camera for board perception
- ArUco markers placed on the board and pieces
- Network connection to robot controllers (IP: 192.168.4.1)

### Configuration

1. Update the serial port in `main.py` (currently set to 'COM3')
2. Update the server IP in `perception.py` if needed (currently '10.168.70.199')
3. Calibrate camera intrinsics in `perception.py` if using a different camera

## Usage

1. Ensure the robotic arms and camera are connected and powered on
2. Run the main script:

```bash
python main.py
```

The system will continuously:
- Capture board state via perception
- Compute the best move using game logic
- Send commands to the robotic arms to execute the move

## Implementation Notes

- `game.py` needs to be implemented with the game AI logic
- `movetocmd()` function in `main.py` needs to convert move strings to robot commands
- Perception uses socket communication to receive camera data
- Commands are sent via HTTP requests to the robot controllers

## Troubleshooting

- Check serial port connections
- Verify camera calibration and ArUco marker detection
- Ensure network connectivity to robot IPs
- Monitor console output for error messages