# Automatic Jumping Height Measuring System 

This project estimates how high a person jumps using a real-time video feed and pose estimation.
It uses MediaPipe to track body landmarks and calculates jump height based on the vertical displacement of the nose landmark.

## Requirements
- Python 3.10
- OpenCv
- MediaPipe

## How to Run
python main.py
- The program will ask for your real height (in meters) for accurate jump height calculation.

- Stand still for the first few seconds to allow calibration.

- Then jump! The height will be shown in pixels and meters.

## How it Works
- Tracks the nose landmark in real-time.

- Records your standing nose height during the first few seconds.

- Calculates jump height as the difference between your standing nose Y and the jump peak Y.

- Converts pixel height to meters using your real height.