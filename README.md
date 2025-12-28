# Virtual Mouse using Hand Tracking

A Python-based virtual mouse that uses hand gestures detected via MediaPipe
to control the system cursor.

## Features
- Cursor movement using index finger
- Left click, right click, and scrolling gestures
- Constant acceleration
- Dead zone to prevent drift
- Toggleable debug drawing (using D key on keyboard)
- Built with OpenCV, MediaPipe, pynput, and pyautogui

## Setup Instructions

```bash
git clone https://github.com/peeyushkumarblw-prog/Virtual-Mouse.git
cd Virtual-Mouse

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
python Basic.py
```

## License

This project is licensed under the MIT License.

Hand tracking logic is inspired by tutorials from  
Murtaza Hassan (Murtaza's Workshop - Robotics and AI).

