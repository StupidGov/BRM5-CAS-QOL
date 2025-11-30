# ============================================================================
#                        crosshair_config_widget.py
# ============================================================================

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QComboBox, QCheckBox, QPushButton, QColorDialog, QGroupBox, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import copy

from crosshair_preview import CrosshairPreview

CROSSHAIR_DEFAULT = {
    "style": "cross",
    "size": 10,
    "thickness": 2,
    "gap": 5,
    "outline_thickness": 1,
    "color": "#00FF00",
    "outline_color": "#000000",
    "center_dot": False,
    "center_dot_size": 2,
    "alpha": 255,
    "t_style": False,
    "draw_outline": True,
}

class CrosshairConfigWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setup_ui()
        self.update_preview()

    def setup_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        controls_layout = QVBoxLayout()

        settings_group = QGroupBox("Crosshair Settings")
        settings_layout = QGridLayout()
        settings_group.setLayout(settings_layout)

        self.create_controls(settings_layout)

        controls_layout.addWidget(settings_group)
        controls_layout.addStretch()

        layout.addLayout(controls_layout)

        preview_layout = QVBoxLayout()
        preview_label = QLabel("Preview")
        preview_label.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(preview_label)

        self.preview = CrosshairPreview()
        preview_layout.addWidget(self.preview)

        layout.addLayout(preview_layout)

    def create_controls(self, layout):
        row = 0

        layout.addWidget(QLabel("Style:"), row, 0)
        self.style_combo = QComboBox()
        self.style_combo.addItems(["cross", "dot", "circle"])
        self.style_combo.setCurrentText(self.config["style"])
        self.style_combo.currentTextChanged.connect(self.update_preview)
        layout.addWidget(self.style_combo, row, 1, 1, 2)
        row += 1

        self.add_slider_row(layout, row, "Size:", "size", 1, 50)
        row += 1

        self.add_slider_row(layout, row, "Thickness:", "thickness", 1, 10)
        row += 1

        self.add_slider_row(layout, row, "Gap:", "gap", 0, 20)
        row += 1

        self.add_slider_row(layout, row, "Outline Thickness:", "outline_thickness", 0, 5)
        row += 1

        self.add_slider_row(layout, row, "Center Dot Size:", "center_dot_size", 1, 10)
        row += 1

        self.add_slider_row(layout, row, "Opacity:", "alpha", 0, 255)
        row += 1

        layout.addWidget(QLabel("Color:"), row, 0)
        self.color_button = QPushButton()
        self.color_button.setFixedSize(100, 30)
        self.color_button.setStyleSheet(f"background-color: {self.config['color']};")
        self.color_button.clicked.connect(self.pick_color)
        layout.addWidget(self.color_button, row, 1)
        row += 1

        layout.addWidget(QLabel("Outline Color:"), row, 0)
        self.outline_color_button = QPushButton()
        self.outline_color_button.setFixedSize(100, 30)
        self.outline_color_button.setStyleSheet(f"background-color: {self.config['outline_color']};")
        self.outline_color_button.clicked.connect(self.pick_outline_color)
        layout.addWidget(self.outline_color_button, row, 1)
        row += 1

        self.center_dot_check = QCheckBox("Center Dot")
        self.center_dot_check.setChecked(self.config["center_dot"])
        self.center_dot_check.stateChanged.connect(self.update_preview)
        layout.addWidget(self.center_dot_check, row, 0, 1, 2)
        row += 1

        self.outline_check = QCheckBox("Draw Outline")
        self.outline_check.setChecked(self.config["draw_outline"])
        self.outline_check.stateChanged.connect(self.update_preview)
        layout.addWidget(self.outline_check, row, 0, 1, 2)
        row += 1

        self.t_style_check = QCheckBox("T-Style (No Top Line)")
        self.t_style_check.setChecked(self.config["t_style"])
        self.t_style_check.stateChanged.connect(self.update_preview)
        layout.addWidget(self.t_style_check, row, 0, 1, 2)

    def add_slider_row(self, layout, row, label_text, config_key, min_val, max_val):
        layout.addWidget(QLabel(label_text), row, 0)

        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(self.config[config_key])
        slider.valueChanged.connect(self.update_preview)

        label = QLabel(str(self.config[config_key]))

        setattr(self, f"{config_key}_slider", slider)
        setattr(self, f"{config_key}_label", label)

        layout.addWidget(slider, row, 1)
        layout.addWidget(label, row, 2)

    def update_preview(self):
        slider_keys = ["size", "thickness", "gap", "outline_thickness", "center_dot_size", "alpha"]
        
        for key in slider_keys:
            slider = getattr(self, f"{key}_slider")
            label = getattr(self, f"{key}_label")
            label.setText(str(slider.value()))
            self.config[key] = slider.value()

        self.config.update({
            "style": self.style_combo.currentText(),
            "center_dot": self.center_dot_check.isChecked(),
            "t_style": self.t_style_check.isChecked(),
            "draw_outline": self.outline_check.isChecked(),
        })

        self.preview.set_config(self.config)

    def pick_color(self):
        color = QColorDialog.getColor(QColor(self.config["color"]), self)
        if color.isValid():
            self.config["color"] = color.name()
            self.color_button.setStyleSheet(f"background-color: {color.name()};")
            self.update_preview()

    def pick_outline_color(self):
        color = QColorDialog.getColor(QColor(self.config["outline_color"]), self)
        if color.isValid():
            self.config["outline_color"] = color.name()
            self.outline_color_button.setStyleSheet(f"background-color: {color.name()};")
            self.update_preview()

    def get_config(self):
        return self.config

    def reset_to_default(self):
        self.config = copy.deepcopy(CROSSHAIR_DEFAULT)

        self.style_combo.setCurrentText(self.config["style"])
        self.size_slider.setValue(self.config["size"])
        self.thickness_slider.setValue(self.config["thickness"])
        self.gap_slider.setValue(self.config["gap"])
        self.outline_thickness_slider.setValue(self.config["outline_thickness"])
        self.center_dot_size_slider.setValue(self.config["center_dot_size"])
        self.alpha_slider.setValue(self.config["alpha"])
        self.center_dot_check.setChecked(self.config["center_dot"])
        self.outline_check.setChecked(self.config["draw_outline"])
        self.t_style_check.setChecked(self.config["t_style"])
        self.color_button.setStyleSheet(f"background-color: {self.config['color']};")
        self.outline_color_button.setStyleSheet(f"background-color: {self.config['outline_color']};")

        self.update_preview()
