# Virtual Mouse using Hand Tracking

A Python-based virtual mouse that uses hand gestures detected via MediaPipe
to control the system cursor.

## Features
- Cursor movement using index finger
- Left click, right click, and scrolling gestures
- Smooth pointer control with constant acceleration
- Dead zone to prevent drift
- Toggleable debug drawing (using D key on keyboard)
- Built with Python, OpenCV, MediaPipe, pynput, and pyautogui

## Requirements

- Python **3.10 – 3.12**  
  *(MediaPipe does not currently support Python 3.13)*
- Python 3.9 may work but MediaPipe can be unstable
- A working webcam
- Supported OS: Windows / macOS / Linux
- Internet connection (for installing dependencies)

## Setup Instructions

```bash
git clone https://github.com/peeyushkumarblw-prog/Virtual-Mouse.git
cd Virtual-Mouse

python -m venv .venv
.venv\Scripts\activate

python -m pip install --upgrade pip

pip install -r requirements.txt
python Basic.py
```

## License

This project is licensed under the MIT License.

Hand tracking logic is inspired by tutorials from  
Murtaza Hassan (Murtaza's Workshop - Robotics and AI).

