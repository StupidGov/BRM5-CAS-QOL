# ============================================================================
#                           crosshair_preview.py
# ============================================================================

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

CANVAS_SIZE = 400
GRID_SPACING = 20
CENTER_X = CANVAS_SIZE // 2
CENTER_Y = CANVAS_SIZE // 2

class CrosshairPreview(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(CANVAS_SIZE, CANVAS_SIZE)
        self.config = {}

    def set_config(self, config):
        self.config = config
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QPen(QColor(60, 60, 60), 1))
        for i in range(0, CANVAS_SIZE, GRID_SPACING):
            painter.drawLine(i, 0, i, CANVAS_SIZE)
            painter.drawLine(0, i, CANVAS_SIZE, i)

        if not self.config:
            return

        style = self.config["style"]
        size = self.config["size"]
        thickness = self.config["thickness"]
        gap = self.config["gap"]
        outline_thickness = self.config["outline_thickness"]
        color = QColor(self.config["color"])
        outline_color = QColor(self.config["outline_color"])
        center_dot = self.config["center_dot"]
        center_dot_size = self.config["center_dot_size"]
        draw_outline = self.config["draw_outline"]
        t_style = self.config["t_style"]
        alpha = self.config["alpha"]

        color.setAlpha(alpha)
        outline_color.setAlpha(alpha)

        if style == "dot":
            self._draw_dot(painter, CENTER_X, CENTER_Y, center_dot_size, color, 
                          outline_color, draw_outline, outline_thickness)

        elif style == "circle":
            self._draw_circle(painter, CENTER_X, CENTER_Y, size, thickness, color,
                            outline_color, draw_outline, outline_thickness,
                            center_dot, center_dot_size)

        else:
            self._draw_cross(painter, CENTER_X, CENTER_Y, size, thickness, gap, color,
                           outline_color, draw_outline, outline_thickness,
                           center_dot, center_dot_size, t_style)

    def _draw_dot(self, painter, cx, cy, dot_size, color, outline_color, 
                  draw_outline, outline_thickness):
        if draw_outline and outline_thickness > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(outline_color)
            r = dot_size + outline_thickness
            painter.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        painter.drawEllipse(cx - dot_size, cy - dot_size, 
                          dot_size * 2, dot_size * 2)

    def _draw_circle(self, painter, cx, cy, radius, thickness, color,
                     outline_color, draw_outline, outline_thickness,
                     center_dot, center_dot_size):
        if draw_outline and outline_thickness > 0:
            painter.setPen(QPen(outline_color, thickness + outline_thickness * 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)

        painter.setPen(QPen(color, thickness))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)

        if center_dot:
            self._draw_dot(painter, cx, cy, center_dot_size, color,
                          outline_color, draw_outline, outline_thickness)

    def _draw_cross(self, painter, cx, cy, size, thickness, gap, color,
                    outline_color, draw_outline, outline_thickness,
                    center_dot, center_dot_size, t_style):
        lines = []

        if not t_style:
            lines.append((cx, cy - gap - size, cx, cy - gap))

        lines.append((cx, cy + gap, cx, cy + gap + size))
        lines.append((cx - gap - size, cy, cx - gap, cy))
        lines.append((cx + gap, cy, cx + gap + size, cy))

        if draw_outline and outline_thickness > 0:
            painter.setPen(QPen(outline_color, thickness + outline_thickness * 2, 
                               Qt.SolidLine, Qt.RoundCap))
            for x1, y1, x2, y2 in lines:
                painter.drawLine(x1, y1, x2, y2)

        painter.setPen(QPen(color, thickness, Qt.SolidLine, Qt.RoundCap))
        for x1, y1, x2, y2 in lines:
            painter.drawLine(x1, y1, x2, y2)

        if center_dot:
            self._draw_dot(painter, cx, cy, center_dot_size, color,
                          outline_color, draw_outline, outline_thickness)