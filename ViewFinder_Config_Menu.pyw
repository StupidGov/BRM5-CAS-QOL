# ============================================================================
#                       ViewFinder Config Menu.py
# ============================================================================

import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QStackedWidget)
from PyQt5.QtCore import Qt

from crosshair_config_widget import CrosshairConfigWidget, CROSSHAIR_DEFAULT
from magnifier_config_widget import MagnifierConfigWidget, MAGNIFIER_DEFAULT

CONFIG_FILE = "viewfinder_config.json"
DEFAULT_CONFIG = {
    "crosshair": CROSSHAIR_DEFAULT.copy(),
    "magnifier": MAGNIFIER_DEFAULT.copy(),
    "keybinds": {
        "auto_detect": "up",
        "hide_all": "right",
        "exit": "down",
        "toggle_magnifier": "m",
        "toggle_crosshair": "c"
    }
}

DARK_THEME = """
QMainWindow, QWidget {
    background-color: #2b2b2b;
    color: #ffffff;
}
QPushButton {
    background-color: #3d3d3d;
    color: #ffffff;
    border: 1px solid #555555;
    padding: 5px 10px;
    border-radius: 3px;
}
QPushButton:checked {
    background-color: #0d7377;
    border: 2px solid #14ffec;
}
QLabel {
    color: #ffffff;
}
QLineEdit, QSpinBox, QDoubleSpinBox {
    background-color: #3d3d3d;
    color: #ffffff;
    border: 1px solid #555555;
    padding: 2px 5px;
}
QSlider::groove:horizontal {
    background: #555555;
    height: 8px;
    border-radius: 4px;
}
QSlider::handle:horizontal {
    background: #0d7377;
    border: 1px solid #14ffec;
    width: 16px;
    margin: -4px 0;
    border-radius: 3px;
}
QCheckBox {
    color: #ffffff;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #555555;
    background-color: #2b2b2b;
}
QCheckBox::indicator:checked {
    background-color: #0d7377;
    border: 1px solid #14ffec;
}
"""

LIGHT_THEME = """
QMainWindow, QWidget {
    background-color: #f0f0f0;
    color: #000000;
}
QPushButton {
    background-color: #e0e0e0;
    color: #000000;
    border: 1px solid #cccccc;
    padding: 5px 10px;
    border-radius: 3px;
}
QPushButton:checked {
    background-color: #4a9eff;
    border: 2px solid #0066cc;
    color: #ffffff;
}
QLabel {
    color: #000000;
}
QLineEdit, QSpinBox, QDoubleSpinBox {
    background-color: #e0e0e0;
    color: #000000;
    border: 1px solid #cccccc;
    padding: 2px 5px;
}
QSlider::groove:horizontal {
    background: #cccccc;
    height: 8px;
    border-radius: 4px;
}
QSlider::handle:horizontal {
    background: #4a9eff;
    border: 1px solid #0066cc;
    width: 16px;
    margin: -4px 0;
    border-radius: 3px;
}
QCheckBox {
    color: #000000;
}
"""

VALID_KEYS = {
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'up', 'down', 'left', 'right',
    'space', 'enter', 'shift', 'ctrl', 'alt', 'tab', 'esc',
    'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12'
}

class KeybindsWidget(QWidget):
    def __init__(self, keybinds):
        super().__init__()
        self.keybinds = keybinds.copy()
        self.inputs = {}
        layout = QVBoxLayout()
        self.setLayout(layout)

        for name, key in self.keybinds.items():
            row = QHBoxLayout()
            label = QLabel(name.replace("_", " ").capitalize() + ":")
            label.setFixedWidth(150)
            edit = QLineEdit(key)
            edit.setFixedWidth(80)
            edit.setMaxLength(10)
            edit.textChanged.connect(lambda text, e=edit: self.validate_key(e, text))
            row.addWidget(label)
            row.addWidget(edit)
            row.addStretch()
            layout.addLayout(row)
            self.inputs[name] = edit

        layout.addStretch()

    def validate_key(self, edit_widget, text):
        text_lower = text.lower().strip()
        if text_lower and text_lower not in VALID_KEYS:
            edit_widget.setStyleSheet("border: 2px solid #ff4444;")
        else:
            edit_widget.setStyleSheet("")

    def get_config(self):
        for name, edit in self.inputs.items():
            self.keybinds[name] = edit.text()
        return self.keybinds

    def reset_to_default(self):
        for name, default_key in DEFAULT_CONFIG["keybinds"].items():
            if name in self.inputs:
                self.inputs[name].setText(default_key)

class MainConfigMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ViewFinder Configuration Menu")
        self.setGeometry(100, 100, 900, 700)

        self.dark_mode = True
        self.current_mode = "crosshair"

        self.config_data = self.load_config(CONFIG_FILE, DEFAULT_CONFIG)

        self.mode_mapping = {
            "crosshair": (0, None),
            "magnifier": (1, None),
            "options": (2, None)
        }

        self.setup_ui()
        self.apply_theme()

    def load_config(self, filepath, default_config):
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    loaded = json.load(f)
                    config = {}
                    for key in default_config:
                        if key in loaded and isinstance(default_config[key], dict):
                            config[key] = {**default_config[key], **loaded[key]}
                        elif key in loaded:
                            config[key] = loaded[key]
                        else:
                            config[key] = default_config[key]
                    return config
            except Exception as e:
                print(f"[WARN] Could not load {filepath}: {e}")
        return {k: v.copy() if isinstance(v, dict) else v for k, v in default_config.items()}

    def save_config(self, filepath, config):
        try:
            with open(filepath, "w") as f:
                json.dump(config, f, indent=4)
            print(f"[INFO] Configuration saved to {filepath}")
            return True
        except Exception as e:
            print(f"[ERROR] Could not save {filepath}: {e}")
            return False

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        tab_layout = QHBoxLayout()

        self.crosshair_tab_btn = QPushButton("Crosshair")
        self.crosshair_tab_btn.setCheckable(True)
        self.crosshair_tab_btn.setChecked(True)
        self.crosshair_tab_btn.clicked.connect(lambda: self.switch_mode("crosshair"))

        self.magnifier_tab_btn = QPushButton("Magnifier")
        self.magnifier_tab_btn.setCheckable(True)
        self.magnifier_tab_btn.setChecked(False)
        self.magnifier_tab_btn.clicked.connect(lambda: self.switch_mode("magnifier"))

        self.options_tab_btn = QPushButton("Options")
        self.options_tab_btn.setCheckable(True)
        self.options_tab_btn.setChecked(False)
        self.options_tab_btn.clicked.connect(lambda: self.switch_mode("options"))

        self.mode_mapping["crosshair"] = (0, self.crosshair_tab_btn)
        self.mode_mapping["magnifier"] = (1, self.magnifier_tab_btn)
        self.mode_mapping["options"] = (2, self.options_tab_btn)

        tab_layout.addWidget(self.crosshair_tab_btn)
        tab_layout.addWidget(self.magnifier_tab_btn)
        tab_layout.addWidget(self.options_tab_btn)
        tab_layout.addStretch()
        main_layout.addLayout(tab_layout)

        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        self.crosshair_widget = CrosshairConfigWidget(self.config_data["crosshair"])
        self.magnifier_widget = MagnifierConfigWidget(self.config_data["magnifier"])
        self.keybinds_widget = KeybindsWidget(self.config_data["keybinds"])

        self.stacked_widget.addWidget(self.crosshair_widget)
        self.stacked_widget.addWidget(self.magnifier_widget)
        self.stacked_widget.addWidget(self.keybinds_widget)

        button_layout = QHBoxLayout()

        save_btn = QPushButton("Save Configuration")
        save_btn.clicked.connect(self.save_current_config)
        button_layout.addWidget(save_btn)

        reset_btn = QPushButton("Reset to Default")
        reset_btn.clicked.connect(self.reset_current_config)
        button_layout.addWidget(reset_btn)

        theme_btn = QPushButton("Toggle Theme")
        theme_btn.clicked.connect(self.toggle_theme)
        button_layout.addWidget(theme_btn)

        apply_btn = QPushButton("Apply & Close")
        apply_btn.clicked.connect(self.apply_and_close)
        button_layout.addWidget(apply_btn)

        main_layout.addLayout(button_layout)

    def switch_mode(self, mode):
        self.current_mode = mode
        for _, (_, btn) in self.mode_mapping.items():
            if btn:
                btn.setChecked(False)

        if mode in self.mode_mapping:
            index, btn = self.mode_mapping[mode]
            self.stacked_widget.setCurrentIndex(index)
            if btn:
                btn.setChecked(True)

    def save_current_config(self):
        self.config_data["crosshair"] = self.crosshair_widget.get_config()
        self.config_data["magnifier"] = self.magnifier_widget.get_config()
        self.config_data["keybinds"] = self.keybinds_widget.get_config()
        self.save_config(CONFIG_FILE, self.config_data)

    def reset_current_config(self):
        reply = QMessageBox.question(
            self, "Reset to Defaults",
            "Are you sure you want to reset all settings to default values?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.crosshair_widget.reset_to_default()
            self.magnifier_widget.reset_to_default()
            self.keybinds_widget.reset_to_default()
            print("[INFO] Reset to defaults")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(DARK_THEME if self.dark_mode else LIGHT_THEME)

    def apply_and_close(self):
        self.save_current_config()
        self.close()

def main():
    app = QApplication(sys.argv)
    window = MainConfigMenu()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()