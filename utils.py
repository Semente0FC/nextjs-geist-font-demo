"""
utils.py

Helper functions for the aimbot system.

Author: BLACKBOXAI
"""

import ctypes
import platform

def hex_to_bgr(hex_color):
    """
    Convert hex color string (#RRGGBB) to BGR tuple for OpenCV.
    """
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError("Invalid hex color format")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (b, g, r)

def move_mouse_to(x, y):
    """
    Move the mouse cursor to (x, y) screen coordinates.
    Supports Windows, macOS, and Linux.
    """
    system = platform.system()
    if system == "Windows":
        ctypes.windll.user32.SetCursorPos(x, y)
    elif system == "Darwin":
        # macOS
        import Quartz.CoreGraphics as CG
        move = CG.CGEventCreateMouseEvent(None, CG.kCGEventMouseMoved, (x, y), CG.kCGMouseButtonLeft)
        CG.CGEventPost(CG.kCGHIDEventTap, move)
    else:
        # Linux (X11)
        import subprocess
        subprocess.run(["xdotool", "mousemove", str(x), str(y)])
