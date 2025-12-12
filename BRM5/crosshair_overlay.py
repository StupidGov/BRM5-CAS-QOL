# ============================================================================
#                         crosshair_overlay.py
# ============================================================================

import tkinter as tk
import ctypes
import threading
import json
import os

MAIN_CONFIG_FILE = "viewfinder_config.json"

DEFAULT_CROSSHAIR_CONFIG = {
    "style": "cross",
    "size": 10,
    "thickness": 2,
    "gap": 5,
    "outline_thickness": 1,
    "color": "#00FF00",
    "outline_color": "#000000",
    "center_dot": True,
    "center_dot_size": 2,
    "alpha": 255,
    "t_style": False,
    "draw_outline": True,
}

class CrosshairOverlay:
    def __init__(self):
        self.root = None
        self.canvas = None
        self.visible = True
        self.position_set = False
        self.lock = threading.Lock()
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(MAIN_CONFIG_FILE):
            try:
                with open(MAIN_CONFIG_FILE, "r") as f:
                    main_config = json.load(f)
                    loaded = main_config.get("crosshair", {})
                    return {**DEFAULT_CROSSHAIR_CONFIG, **loaded}
            except Exception as e:
                print(f"[WARN] Could not load crosshair config from {MAIN_CONFIG_FILE}: {e}")
        return DEFAULT_CROSSHAIR_CONFIG.copy()

    def setup(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', 'white')

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        self.canvas = tk.Canvas(self.root, bg='white', highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        cx = screen_width // 2
        cy = screen_height // 2
        self.draw_crosshair(cx, cy)

        self.root.update_idletasks()

        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        GWL_EXSTYLE = -20
        WS_EX_TRANSPARENT = 0x20
        WS_EX_LAYERED = 0x80000
        styles = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, 
                                            styles | WS_EX_TRANSPARENT | WS_EX_LAYERED)

        self.position_set = True
        self.root.mainloop()

    def draw_center_dot(self, cx, cy, dot_size, color, outline_color, outline_thickness, draw_outline):
        if draw_outline and outline_thickness > 0:
            r = dot_size + outline_thickness
            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=outline_color, outline=outline_color)
        self.canvas.create_oval(cx - dot_size, cy - dot_size, cx + dot_size, cy + dot_size, fill=color, outline=color)

    def draw_crosshair(self, cx, cy):
        cfg = self.config
        style = cfg["style"]
        size = cfg["size"]
        thickness = cfg["thickness"]
        gap = cfg["gap"]
        color = cfg["color"]
        outline_color = cfg["outline_color"]
        outline_thickness = cfg["outline_thickness"]
        draw_outline = cfg["draw_outline"]
        center_dot = cfg["center_dot"]
        center_dot_size = cfg["center_dot_size"]
        t_style = cfg["t_style"]

        if style == "dot":
            self.draw_center_dot(cx, cy, center_dot_size, color, outline_color, outline_thickness, draw_outline)

        elif style == "circle":
            if draw_outline and outline_thickness > 0:
                self.canvas.create_oval(cx - size - outline_thickness, cy - size - outline_thickness, 
                                       cx + size + outline_thickness, cy + size + outline_thickness, 
                                       outline=outline_color, width=thickness + outline_thickness * 2)
            self.canvas.create_oval(cx - size, cy - size, cx + size, cy + size, outline=color, width=thickness)

            if center_dot:
                self.draw_center_dot(cx, cy, center_dot_size, color, outline_color, outline_thickness, draw_outline)

        else:
            lines = []

            if not t_style:
                lines.append((cx, cy - gap - size, cx, cy - gap))

            lines.append((cx, cy + gap, cx, cy + gap + size))
            lines.append((cx - gap - size, cy, cx - gap, cy))
            lines.append((cx + gap, cy, cx + gap + size, cy))

            if draw_outline and outline_thickness > 0:
                for x1, y1, x2, y2 in lines:
                    self.canvas.create_line(x1, y1, x2, y2, fill=outline_color, 
                                          width=thickness + outline_thickness * 2, capstyle=tk.ROUND)

            for x1, y1, x2, y2 in lines:
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=thickness, capstyle=tk.ROUND)

            if center_dot:
                self.draw_center_dot(cx, cy, center_dot_size, color, outline_color, outline_thickness, draw_outline)

    def set_visibility(self, visible):
        with self.lock:
            if self.position_set and self.canvas and self.root:
                try:
                    if visible:
                        self.root.after(0, lambda: self.root.deiconify())
                    else:
                        self.root.after(0, lambda: self.root.withdraw())
                    self.visible = visible
                except Exception as e:
                    print(f"[WARN] Crosshair visibility update failed: {e}")

    def quit(self):
        if self.root:
            self.root.quit()

def start_crosshair_thread():
    overlay = CrosshairOverlay()
    thread = threading.Thread(target=overlay.setup, daemon=True)
    thread.start()
    return overlay