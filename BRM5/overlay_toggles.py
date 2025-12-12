# ============================================================================
#                           overlay_toggles.py
# ============================================================================

from PyQt5.QtCore import QObject, pyqtSignal

class OverlayToggles(QObject):
    toggle_magnifier_signal = pyqtSignal()
    toggle_crosshair_signal = pyqtSignal()

    def __init__(self, magnifier_overlay, crosshair_overlay):
        super().__init__()
        self.magnifier_overlay = magnifier_overlay
        self.crosshair_overlay = crosshair_overlay
        self.magnifier_visible = True
        self.crosshair_visible = True

        self.toggle_magnifier_signal.connect(self._toggle_magnifier)
        self.toggle_crosshair_signal.connect(self._toggle_crosshair)

    def _toggle_overlay(self, overlay, is_visible, name):
        if overlay is None:
            print(f"[WARN] {name} overlay not initialized")
            return False
        try:
            overlay.set_visibility(is_visible)
            print(f"[INFO] {name} {'ON' if is_visible else 'OFF'}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to toggle {name}: {e}")
            return False

    def _toggle_magnifier(self):
        self.magnifier_visible = not self.magnifier_visible
        if not self._toggle_overlay(self.magnifier_overlay, self.magnifier_visible, "Magnifier"):
            self.magnifier_visible = not self.magnifier_visible

    def _toggle_crosshair(self):
        self.crosshair_visible = not self.crosshair_visible
        if not self._toggle_overlay(self.crosshair_overlay, self.crosshair_visible, "Crosshair"):
            self.crosshair_visible = not self.crosshair_visible


