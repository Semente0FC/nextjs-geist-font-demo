"""
aimbot.py

Main logic for color-based aimbot system using OpenCV.
Captures screen, detects target color within FOV, applies vertical offset,
and moves mouse cursor to aim automatically.

Author: BLACKBOXAI
"""

import cv2
import numpy as np
import threading
import time
from utils import hex_to_bgr, move_mouse_to
from screen_capture import grab_screen

class Aimbot:
    def __init__(self, aim_color_hex="#FF0C0C", fov_radius=100, vertical_offset=0, enabled=False):
        self.aim_color_hex = aim_color_hex
        self.aim_color_bgr = hex_to_bgr(aim_color_hex)
        self.fov_radius = fov_radius
        self.vertical_offset = vertical_offset
        self.enabled = enabled
        self.screen_width, self.screen_height = grab_screen.get_screen_size()
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        self.running = False

    def update_settings(self, aim_color_hex=None, fov_radius=None, vertical_offset=None, enabled=None):
        if aim_color_hex is not None:
            self.aim_color_hex = aim_color_hex
            self.aim_color_bgr = hex_to_bgr(aim_color_hex)
        if fov_radius is not None:
            self.fov_radius = fov_radius
        if vertical_offset is not None:
            self.vertical_offset = vertical_offset
        if enabled is not None:
            self.enabled = enabled

    def _run(self):
        while self.running:
            if not self.enabled:
                time.sleep(0.1)
                continue

            frame = grab_screen.capture()
            if frame is None:
                time.sleep(0.1)
                continue

            # Detect target color within FOV circle
            target_point = self._detect_target(frame)
            if target_point:
                aim_x, aim_y = target_point
                # Apply vertical offset
                aim_y = max(0, aim_y - self.vertical_offset)
                # Move mouse cursor to aim point
                move_mouse_to(aim_x, aim_y)

            time.sleep(0.01)

    def _run_preview_frame(self):
        """
        Capture a frame and draw FOV circle and detected target for preview.
        Returns the frame with drawings.
        """
        frame = grab_screen.capture()
        if frame is None:
            return None

        # Draw FOV circle
        cv2.circle(frame, (self.center_x, self.center_y), self.fov_radius, (255, 255, 255), 2)

        # Detect target color within FOV
        target_point = self._detect_target(frame)
        if target_point:
            cv2.circle(frame, target_point, 10, (0, 255, 0), 3)

        return frame

    def _detect_target(self, frame):
        # Convert frame to HSV for better color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Convert aim color BGR to HSV
        color_bgr = np.uint8([[self.aim_color_bgr]])
        color_hsv = cv2.cvtColor(color_bgr, cv2.COLOR_BGR2HSV)[0][0]

        # Define range for color detection
        lower_bound = np.array([max(0, color_hsv[0] - 10), 100, 100])
        upper_bound = np.array([min(179, color_hsv[0] + 10), 255, 255])

        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        # Mask with FOV circle
        mask_circle = np.zeros_like(mask)
        cv2.circle(mask_circle, (self.center_x, self.center_y), self.fov_radius, 255, -1)
        mask = cv2.bitwise_and(mask, mask_circle)

        # Find contours of detected color areas
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None

        # Find largest contour center as target
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M["m00"] == 0:
            return None
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        return (cX, cY)

if __name__ == "__main__":
    # For testing purposes
    aimbot = Aimbot()
    aimbot.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        aimbot.stop()
