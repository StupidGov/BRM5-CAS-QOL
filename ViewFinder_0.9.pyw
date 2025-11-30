# ============================================================================
#                           ViewFinder_0.9.py
# ============================================================================
import sys
import time
import cv2
import numpy as np
from mss import mss
import threading
import json
import os
import traceback

try:
    import keyboard
    _HAS_KEYBOARD = True
except ImportError:
    _HAS_KEYBOARD = False
    print("[WARN] 'keyboard' library not found. Install with: pip install keyboard")
    sys.exit(1)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QObject, pyqtSignal

from crosshair_overlay import start_crosshair_thread
from magnifier_overlay import MagnifierOverlay
from overlay_toggles import OverlayToggles
from instructions_menu import InstructionsMenu

CONFIG_FILE = "viewfinder_config.json"
DEFAULT_CONFIG = {
    "crosshair": {},
    "magnifier": {},
    "keybinds": {
        "auto_detect": "up",
        "hide_all": "right",
        "exit": "down",
        "toggle_magnifier": "m",
        "toggle_crosshair": "c"
    }
}

DETECTION_CHECK_MS = 100
mss_global = mss()

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                loaded = json.load(f)
                config = {}
                for key in DEFAULT_CONFIG:
                    if key in loaded and isinstance(DEFAULT_CONFIG[key], dict):
                        config[key] = {**DEFAULT_CONFIG[key], **loaded[key]}
                    elif key in loaded:
                        config[key] = loaded[key]
                    else:
                        config[key] = DEFAULT_CONFIG[key]
                return config
        except Exception as e:
            print(f"[WARN] Could not load config: {e}")
            traceback.print_exc()
    return {k: v.copy() if isinstance(v, dict) else v for k, v in DEFAULT_CONFIG.items()}

def detect_yellow_in_region(mag_detection_pos):
    x, y = mag_detection_pos
    region = {"left": x - 2, "top": y - 2, "width": 5, "height": 5}
    try:
        sct_img = mss_global.grab(region)
        frame = np.array(sct_img)[..., :3]
        b = frame[:, :, 0]
        g = frame[:, :, 1]
        r = frame[:, :, 2]
        yellow_mask = (r > 150) & (g > 150) & (b < 140)
        return np.count_nonzero(yellow_mask) > 1
    except Exception as e:
        print(f"[WARN] Detection failed: {e}")
        return False

class VisibilityController:
    def __init__(self, magnifier_overlay, crosshair_overlay, mag_detection_pos):
        self.magnifier_overlay = magnifier_overlay
        self.crosshair_overlay = crosshair_overlay
        self.mag_detection_pos = mag_detection_pos
        self.auto_detect_enabled = False
        self.last_detection_state = None
        self.toggle_lock = threading.Lock()
        self.last_toggle_time = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_and_update)
        self.timer.start(DETECTION_CHECK_MS)

    def toggle_auto_detect(self):
        current_time = time.time()
        with self.toggle_lock:
            if current_time - self.last_toggle_time < 0.3:
                return
            self.last_toggle_time = current_time
            self.auto_detect_enabled = not self.auto_detect_enabled
        if self.auto_detect_enabled:
            print("[INFO] Auto-detection ENABLED")
            self.last_detection_state = None
        else:
            print("[INFO] Auto-detection DISABLED")
            self.force_show()
            self.last_detection_state = None

    def _set_overlay_visibility(self, overlay, visible, name):
        try:
            overlay.set_visibility(visible)
        except Exception as e:
            print(f"[WARN] {name} visibility change failed: {e}")

    def force_show(self):
        if self.magnifier_overlay:
            self._set_overlay_visibility(self.magnifier_overlay, True, "magnifier")
        if self.crosshair_overlay:
            self._set_overlay_visibility(self.crosshair_overlay, True, "crosshair")

    def force_hide(self):
        if self.magnifier_overlay:
            self._set_overlay_visibility(self.magnifier_overlay, False, "magnifier")
        if self.crosshair_overlay:
            self._set_overlay_visibility(self.crosshair_overlay, False, "crosshair")

    def check_and_update(self):
        if not self.auto_detect_enabled:
            return
        try:
            yellow_detected = detect_yellow_in_region(self.mag_detection_pos)
            if yellow_detected != self.last_detection_state:
                if yellow_detected:
                    self.force_show()
                    print("[INFO] Gun equipped - showing overlays")
                else:
                    self.force_hide()
                    print("[INFO] Gun holstered - hiding overlays")
                self.last_detection_state = yellow_detected
        except Exception as e:
            print(f"[WARN] Check failed: {e}")

class GuiDispatcher(QObject):
    toggle_all_signal = pyqtSignal()
    toggle_auto_signal = pyqtSignal()
    exit_signal = pyqtSignal()

def format_key_name(key):
    if len(key) == 1:
        return key.upper()
    return key.capitalize()

def main():
    print("[INFO] Starting overlay system...")

    config = load_config()

    keybinds = config.get("keybinds", {})
    auto_detect_key = keybinds.get("auto_detect", "up")
    hide_all_key = keybinds.get("hide_all", "right")
    exit_key = keybinds.get("exit", "down")
    crosshair_key = keybinds.get("toggle_crosshair", "c")
    magnifier_key = keybinds.get("toggle_magnifier", "m")

    mag_config = config.get("magnifier", {})
    mag_detection_pos = tuple(mag_config.get("mag_detection_pos", [1718, 877]))

    app = QApplication(sys.argv)

    try:
        magnifier_overlay = MagnifierOverlay(config=mag_config)
        magnifier_overlay.create_windows()
    except Exception as e:
        print(f"[ERROR] Magnifier overlay failed: {e}")
        traceback.print_exc()
        magnifier_overlay = None

    try:
        crosshair_overlay = start_crosshair_thread()
        time.sleep(0.5)
    except Exception as e:
        print(f"[ERROR] Crosshair overlay failed: {e}")
        traceback.print_exc()
        crosshair_overlay = None

    try:
        menu = InstructionsMenu()
        menu.show_in_top_right()
    except Exception as e:
        print(f"[ERROR] Instructions menu failed: {e}")
        traceback.print_exc()
        menu = None

    visibility_controller = VisibilityController(
        magnifier_overlay,
        crosshair_overlay,
        mag_detection_pos
    )

    overlay_toggles = OverlayToggles(magnifier_overlay, crosshair_overlay)

    all_hidden_state = False
    previous_auto_detect_state = False
    gui = GuiDispatcher()

    def _do_toggle_all_visibility():
        nonlocal all_hidden_state, previous_auto_detect_state
        all_hidden_state = not all_hidden_state
        if all_hidden_state:
            previous_auto_detect_state = visibility_controller.auto_detect_enabled
            visibility_controller.auto_detect_enabled = False
            visibility_controller.last_detection_state = None
            if magnifier_overlay:
                magnifier_overlay.set_visibility(False)
            if crosshair_overlay:
                crosshair_overlay.set_visibility(False)
            if menu:
                menu.hide()
            QApplication.processEvents()
            print("[INFO] Hiding ALL overlays (manual override)")
        else:
            visibility_controller.auto_detect_enabled = previous_auto_detect_state
            visibility_controller.last_detection_state = None
            if magnifier_overlay:
                magnifier_overlay.set_visibility(True)
            if crosshair_overlay:
                crosshair_overlay.set_visibility(True)
            if menu:
                menu.show()
                menu.show_in_top_right()
            QApplication.processEvents()
            print("[INFO] Restoring ALL overlays")

    def _do_toggle_auto():
        visibility_controller.toggle_auto_detect()

    def _do_exit():
        print("[INFO] Exiting...")
        try:
            keyboard.unhook_all()
        except Exception:
            pass
        try:
            if crosshair_overlay:
                crosshair_overlay.quit()
        except Exception:
            pass
        try:
            app.quit()
        except Exception:
            pass
        sys.exit(0)

    gui.toggle_all_signal.connect(_do_toggle_all_visibility)
    gui.toggle_auto_signal.connect(_do_toggle_auto)
    gui.exit_signal.connect(_do_exit)

    def key_poller():
        debounce_times = {
            auto_detect_key: 0,
            hide_all_key: 0,
            exit_key: 0,
            crosshair_key: 0,
            magnifier_key: 0
        }
        while True:
            now = time.time()
            if keyboard.is_pressed(auto_detect_key) and now - debounce_times[auto_detect_key] > 0.2:
                gui.toggle_auto_signal.emit()
                debounce_times[auto_detect_key] = now
            if keyboard.is_pressed(hide_all_key) and now - debounce_times[hide_all_key] > 0.2:
                gui.toggle_all_signal.emit()
                debounce_times[hide_all_key] = now
            if keyboard.is_pressed(exit_key) and now - debounce_times[exit_key] > 0.2:
                gui.exit_signal.emit()
                debounce_times[exit_key] = now
            if keyboard.is_pressed(magnifier_key) and now - debounce_times[magnifier_key] > 0.2:
                overlay_toggles.toggle_magnifier_signal.emit()
                debounce_times[magnifier_key] = now
            if keyboard.is_pressed(crosshair_key) and now - debounce_times[crosshair_key] > 0.2:
                overlay_toggles.toggle_crosshair_signal.emit()
                debounce_times[crosshair_key] = now
            time.sleep(0.01)

    threading.Thread(target=key_poller, daemon=True).start()

    print("[INFO] Overlays active")
    print(f"[INFO] Detection position: {mag_detection_pos}")
    print("[INFO] Auto-detection is OFF by default")
    print(f"[INFO] Hotkeys:")
    print(f"  - {format_key_name(auto_detect_key)}: Toggle auto-detection")
    print(f"  - {format_key_name(exit_key)}: Exit")
    print(f"  - {format_key_name(hide_all_key)}: Hide all overlays")
    print(f"  - {format_key_name(magnifier_key)}: Toggle magnifier")
    print(f"  - {format_key_name(crosshair_key)}: Toggle crosshair")
    print("[INFO] Running...")

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


