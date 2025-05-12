"""
screen_capture.py

Module to capture the screen for the aimbot system.

Author: BLACKBOXAI
"""

import numpy as np
import cv2
import platform

if platform.system() == "Windows":
    import ctypes
    from PIL import ImageGrab
elif platform.system() == "Darwin":
    from PIL import ImageGrab
else:
    # For Linux, use X11 or fallback
    import subprocess
    import time

def get_screen_size():
    """
    Returns the screen width and height.
    """
    system = platform.system()
    if system == "Windows":
        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    elif system == "Darwin":
        from AppKit import NSScreen
        frame = NSScreen.screens()[0].frame()
        return int(frame.size.width), int(frame.size.height)
    else:
        # Linux fallback using xrandr
        try:
            output = subprocess.check_output("xrandr | grep '*' | awk '{print $1}'", shell=True)
            resolution = output.decode().split()[0]
            width, height = resolution.split('x')
            return int(width), int(height)
        except Exception:
            # Default fallback
            return 1920, 1080

def capture():
    """
    Capture the screen and return as a numpy BGR image.
    """
    system = platform.system()
    if system == "Windows" or system == "Darwin":
        img = ImageGrab.grab()
        img_np = np.array(img)
        # Convert RGB to BGR
        frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        return frame
    else:
        # Linux fallback using scrot and reading file
        filename = "/tmp/screenshot.png"
        subprocess.run(["scrot", filename])
        time.sleep(0.1)
        frame = cv2.imread(filename)
        return frame
