# ============================================================================
#                          instructions_menu.py
# ============================================================================

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QPainter, QColor
import json
import os

DEFAULT_KEYBINDS = {
    "auto_detect": "up",
    "hide_all": "right",
    "exit": "down",
    "toggle_magnifier": "m",
    "toggle_crosshair": "c"
}

class InstructionsMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.NoDropShadowWindowHint
        )

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

        self.dragging = False
        self.drag_position = QPoint()

        self.bg_color = QColor(20, 20, 20, 150)

        keybinds = self.load_keybinds()

        text = (
            "--------- Instructions ---------\n"
            f"    {keybinds['auto_detect']} - Toggle auto-detect\n"
            f"    {keybinds['exit']} - Exit application\n"
            f"    {keybinds['hide_all']} - Toggle all overlays\n"
            f"    {keybinds['toggle_magnifier']} - Toggle magnifier\n"
            f"    {keybinds['toggle_crosshair']} - Toggle crosshair\n"
            "----------------------------------"
        )

        label = QLabel(text)
        label.setStyleSheet("color: white;")
        label.setFont(QFont("Arial", 12))

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(layout)

        self.resize(220, 120)

    def load_keybinds(self):
        config_file = "viewfinder_config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    return config.get("keybinds", DEFAULT_KEYBINDS)
            except Exception as e:
                print(f"[WARN] Could not load keybinds from config: {e}")
        return DEFAULT_KEYBINDS

    def show_in_top_right(self):
        screen = self.screen().availableGeometry()
        x = screen.right() - self.width() - 20
        y = screen.top() + 20
        self.move(x, y)
        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setBrush(self.bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 12, 12)


