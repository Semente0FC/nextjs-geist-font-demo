"""
gui.py

PyQt5 GUI for the color-based aimbot system.
Includes inputs for aim color, FOV radius, vertical offset,
toggle for enabling aim, and real-time preview.

Author: BLACKBOXAI
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QSlider, QVBoxLayout,
    QHBoxLayout, QPushButton, QCheckBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen
import cv2
from aimbot import Aimbot

class AimbotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color-Based Aimbot")
        self.aimbot = Aimbot()
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_preview)
        self.timer.start(30)  # approx 30 FPS

    def init_ui(self):
        layout = QVBoxLayout()

        # Aim Color Input
        color_layout = QHBoxLayout()
        color_label = QLabel("Aim Color (#RRGGBB):")
        self.color_input = QLineEdit("#FF0C0C")
        self.color_input.textChanged.connect(self.on_color_change)
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_input)
        layout.addLayout(color_layout)

        # FOV Radius Slider
        fov_layout = QHBoxLayout()
        fov_label = QLabel("FOV Radius:")
        self.fov_slider = QSlider(Qt.Horizontal)
        self.fov_slider.setMinimum(50)
        self.fov_slider.setMaximum(500)
        self.fov_slider.setValue(100)
        self.fov_slider.valueChanged.connect(self.on_fov_change)
        self.fov_value_label = QLabel(str(self.fov_slider.value()))
        fov_layout.addWidget(fov_label)
        fov_layout.addWidget(self.fov_slider)
        fov_layout.addWidget(self.fov_value_label)
        layout.addLayout(fov_layout)

        # Vertical Offset Slider
        offset_layout = QHBoxLayout()
        offset_label = QLabel("Vertical Offset (pixels):")
        self.offset_slider = QSlider(Qt.Horizontal)
        self.offset_slider.setMinimum(0)
        self.offset_slider.setMaximum(200)
        self.offset_slider.setValue(0)
        self.offset_slider.valueChanged.connect(self.on_offset_change)
        self.offset_value_label = QLabel(str(self.offset_slider.value()))
        offset_layout.addWidget(offset_label)
        offset_layout.addWidget(self.offset_slider)
        offset_layout.addWidget(self.offset_value_label)
        layout.addLayout(offset_layout)

        # Enable Aim Toggle
        self.enable_checkbox = QCheckBox("Enable Aim")
        self.enable_checkbox.stateChanged.connect(self.on_enable_toggle)
        layout.addWidget(self.enable_checkbox)

        # Preview Label
        self.preview_label = QLabel()
        self.preview_label.setFixedSize(640, 480)
        layout.addWidget(self.preview_label)

        self.setLayout(layout)

    def on_color_change(self, text):
        try:
            if len(text) == 7 and text.startswith("#"):
                self.aimbot.update_settings(aim_color_hex=text)
        except Exception:
            pass

    def on_fov_change(self, value):
        self.fov_value_label.setText(str(value))
        self.aimbot.update_settings(fov_radius=value)

    def on_offset_change(self, value):
        self.offset_value_label.setText(str(value))
        self.aimbot.update_settings(vertical_offset=value)

    def on_enable_toggle(self, state):
        enabled = state == Qt.Checked
        self.aimbot.update_settings(enabled=enabled)
        if enabled:
            self.aimbot.start()
        else:
            self.aimbot.stop()

    def update_preview(self):
        frame = self.aimbot._run_preview_frame()
        if frame is not None:
            # Convert frame to QImage and display
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            from PyQt5.QtGui import QImage, QPixmap
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.preview_label.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = AimbotGUI()
    gui.show()
    sys.exit(app.exec_())
