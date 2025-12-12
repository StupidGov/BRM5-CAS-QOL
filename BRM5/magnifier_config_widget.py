# ============================================================================
#                       magnifier_config_widget.py
# ============================================================================

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QSpinBox, QDoubleSpinBox, QGroupBox)
from PyQt5.QtCore import Qt
import copy

MAGNIFIER_DEFAULT = {
    "scale": 2.0,
    "radius": 120,
    "window_size": 400,
    "timer_ms": 33,
    "mag_detection_pos": [1718, 877]
}

RADIUS_RANGE = (50, 300)
RADIUS_TICK = 50
WINDOW_RANGE = (200, 800)
WINDOW_TICK = 100
FPS_RANGE = (10, 60)
FPS_TICK = 10

class MagnifierConfigWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = copy.deepcopy(config)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        mag_group = QGroupBox("Magnification Settings")
        mag_layout = QVBoxLayout()

        scale_layout = QHBoxLayout()
        scale_label = QLabel("Zoom Level:")
        scale_label.setFixedWidth(150)
        self.scale_spinbox = QDoubleSpinBox()
        self.scale_spinbox.setRange(0.1, 10.0)
        self.scale_spinbox.setSingleStep(0.1)
        self.scale_spinbox.setValue(self.config["scale"])
        self.scale_spinbox.setSuffix("x")
        scale_layout.addWidget(scale_label)
        scale_layout.addWidget(self.scale_spinbox)
        mag_layout.addLayout(scale_layout)

        self.radius_slider, self.radius_spinbox = self.create_slider_spinbox_pair(
            mag_layout, "Capture Area Radius:", RADIUS_RANGE, RADIUS_TICK,
            self.config["radius"], " px"
        )

        self.window_slider, self.window_spinbox = self.create_slider_spinbox_pair(
            mag_layout, "Display Window Size:", WINDOW_RANGE, WINDOW_TICK,
            self.config["window_size"], " px"
        )

        current_fps = int(1000 / self.config["timer_ms"])
        self.fps_slider, self.fps_spinbox = self.create_slider_spinbox_pair(
            mag_layout, "Refresh Rate (FPS):", FPS_RANGE, FPS_TICK,
            current_fps, " fps"
        )

        mag_group.setLayout(mag_layout)
        layout.addWidget(mag_group)

        detect_group = QGroupBox("Auto-Detection Settings")
        detect_layout = QVBoxLayout()

        pos_x_layout = QHBoxLayout()
        pos_x_label = QLabel("Detection X Position:")
        pos_x_label.setFixedWidth(150)
        self.pos_x_spinbox = QSpinBox()
        self.pos_x_spinbox.setRange(0, 3840)
        self.pos_x_spinbox.setValue(self.config["mag_detection_pos"][0])
        self.pos_x_spinbox.setSuffix(" px")
        pos_x_layout.addWidget(pos_x_label)
        pos_x_layout.addWidget(self.pos_x_spinbox)
        pos_x_layout.addStretch()
        detect_layout.addLayout(pos_x_layout)

        pos_y_layout = QHBoxLayout()
        pos_y_label = QLabel("Detection Y Position:")
        pos_y_label.setFixedWidth(150)
        self.pos_y_spinbox = QSpinBox()
        self.pos_y_spinbox.setRange(0, 2160)
        self.pos_y_spinbox.setValue(self.config["mag_detection_pos"][1])
        self.pos_y_spinbox.setSuffix(" px")
        pos_y_layout.addWidget(pos_y_label)
        pos_y_layout.addWidget(self.pos_y_spinbox)
        pos_y_layout.addStretch()
        detect_layout.addLayout(pos_y_layout)

        detect_group.setLayout(detect_layout)
        layout.addWidget(detect_group)

        layout.addStretch()

    def create_slider_spinbox_pair(self, parent_layout, label_text, value_range, tick_interval, initial_value, suffix):
        row_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setFixedWidth(150)

        slider = QSlider(Qt.Horizontal)
        slider.setRange(*value_range)
        slider.setValue(initial_value)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(tick_interval)

        spinbox = QSpinBox()
        spinbox.setRange(*value_range)
        spinbox.setValue(initial_value)
        spinbox.setSuffix(suffix)

        slider.valueChanged.connect(spinbox.setValue)
        spinbox.valueChanged.connect(slider.setValue)

        row_layout.addWidget(label)
        row_layout.addWidget(slider)
        row_layout.addWidget(spinbox)
        parent_layout.addLayout(row_layout)

        return slider, spinbox

    def get_config(self):
        self.config["scale"] = self.scale_spinbox.value()
        self.config["radius"] = self.radius_spinbox.value()
        self.config["window_size"] = self.window_spinbox.value()
        self.config["timer_ms"] = int(1000 / self.fps_spinbox.value())
        self.config["mag_detection_pos"] = [
            self.pos_x_spinbox.value(),
            self.pos_y_spinbox.value()
        ]
        return self.config

    def reset_to_default(self):
        self.config = copy.deepcopy(MAGNIFIER_DEFAULT)

        self.scale_spinbox.setValue(self.config["scale"])
        self.radius_spinbox.setValue(self.config["radius"])
        self.window_spinbox.setValue(self.config["window_size"])
        self.fps_spinbox.setValue(int(1000 / self.config["timer_ms"]))
        self.pos_x_spinbox.setValue(self.config["mag_detection_pos"][0])
        self.pos_y_spinbox.setValue(self.config["mag_detection_pos"][1])