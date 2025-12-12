# ============================================================================
#                           magnifier_overlay.py
# ============================================================================

import sys
import cv2
import numpy as np
from mss import mss
import json
import os

from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap, QImage, QCursor
from PyQt5.QtCore import Qt, QTimer

MAIN_CONFIG_FILE = "viewfinder_config.json"

DEFAULT_MAGNIFIER_CONFIG = {
    "scale": 2,
    "radius": 120,
    "window_size": 400,
    "timer_ms": 33,
    "mag_detection_pos": [1718, 877]
}

class MagnifierOverlay:
    def __init__(self, config=None):
        self.config = config if config is not None else self.load_config()
        self.sct = mss()
        self.magnified_window = None
        self.lens_window = None

    def load_config(self):
        if os.path.exists(MAIN_CONFIG_FILE):
            try:
                with open(MAIN_CONFIG_FILE, "r") as f:
                    main_config = json.load(f)
                    loaded_magnifier = main_config.get("magnifier", {})
                    return {**DEFAULT_MAGNIFIER_CONFIG, **loaded_magnifier}
            except Exception as e:
                print(f"[WARN] Could not load magnifier config from {MAIN_CONFIG_FILE}: {e}")
        return DEFAULT_MAGNIFIER_CONFIG.copy()

    def create_windows(self):
        try:
            self.magnified_window = MagnifiedView(self.config["window_size"])
            self.lens_window = LensWindow(
                self.magnified_window,
                self.sct,
                self.config["scale"],
                self.config["radius"],
                self.config["timer_ms"]
            )
            self.magnified_window.show()
            self.lens_window.show()
        except Exception as e:
            print(f"[ERROR] Failed to create magnifier windows: {e}")

    def set_visibility(self, visible):
        if self.magnified_window and self.lens_window:
            if visible:
                if not self.magnified_window.isVisible():
                    self.magnified_window.show()
                if not self.lens_window.isVisible():
                    self.lens_window.show()
            else:
                if self.magnified_window.isVisible():
                    self.magnified_window.hide()
                if self.lens_window.isVisible():
                    self.lens_window.hide()

    def reload_config(self, config=None):
        self.config = config if config is not None else self.load_config()
        if self.magnified_window:
            self.magnified_window.close()
        if self.lens_window:
            self.lens_window.close()
        self.create_windows()

class MagnifiedView(QWidget):
    def __init__(self, window_size):
        super().__init__()
        self.setWindowTitle("Magnified View")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.window_size = window_size

        self._drag_pos = None

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setFixedSize(window_size, window_size)
        self.label.resize(self.size())

    def update_image(self, frame_bgr):
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        qimg = QImage(frame_rgb.data, w, h, ch * w, QImage.Format_RGB888).copy()
        pixmap = QPixmap.fromImage(qimg)

        if w < self.window_size or h < self.window_size:
            pixmap = pixmap.scaled(self.window_size, self.window_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.label.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self._drag_pos:
            self.move(self.pos() + event.globalPos() - self._drag_pos)
            self._drag_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

class LensWindow(QWidget):
    def __init__(self, magnified_window, sct, scale, radius, timer_ms):
        super().__init__()
        self.magnified_window = magnified_window
        self.sct = sct
        self.scale = scale
        self.radius = radius

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.WindowTransparentForInput
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.label.setStyleSheet("background: transparent;")
        self.label.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedSize(radius * 2, radius * 2)
        self.label.resize(self.size())

        self.border_overlay = np.zeros((radius * 2, radius * 2, 4), dtype=np.uint8)
        cv2.rectangle(self.border_overlay, (0, 0), (radius * 2 - 1, radius * 2 - 1), (0, 255, 0, 255), 3)

        w, h = radius * 2, radius * 2
        qimg = QImage(self.border_overlay.data, w, h, 4 * w, QImage.Format_RGBA8888).copy()
        self.border_pixmap = QPixmap.fromImage(qimg)
        self.label.setPixmap(self.border_pixmap)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(timer_ms)

    def update_frame(self):
        pos = QCursor.pos()
        x, y = pos.x(), pos.y()
        self.move(x - self.radius, y - self.radius)

        mon = {
            "left": x - self.radius,
            "top": y - self.radius,
            "width": self.radius * 2,
            "height": self.radius * 2,
        }

        try:
            sct_img = self.sct.grab(mon)
            frame = np.array(sct_img)[..., :3]
            magnified = cv2.resize(frame, None, fx=self.scale, fy=self.scale, interpolation=cv2.INTER_LINEAR)
            self.magnified_window.update_image(magnified)
        except Exception as e:
            print(f"[WARN] Capture failed: {e}")