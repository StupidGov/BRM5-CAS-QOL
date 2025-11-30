# ViewFinder

A lightweight quality-of-life utility for **Blackhawk Rescue Mission 5** on Roblox.

**ViewFinder** provides an on-screen **crosshair overlay** and a **magnifier window** to improve visibility when operating mainly helicopter-mounted weapons — addressing the lack of a built-in crosshair and limited zoom options.

This tool is fully **external**, **non-intrusive**, and safe to use.

***The tool is still in developement***

---

## Why This Tool Was Created

BRM5's helicopter door guns offer no native crosshair and no meaningful zoom for long-range engagement.

This utility adds:
- A reliable, centered, and fully customizable crosshair
- A magnified view of the selected area on your screen with adjustable zoom levels
- Individual overlay toggles for maximum flexibility

Together, they make aiming and target identification far easier during air support operations.

---

## Main Features

### ✓ Customizable Crosshair Overlay
- Multiple styles: cross, dot, and circle
- Adjustable size, thickness, gap, and opacity
- Custom colors for crosshair and outline
- Optional center dot and T-style (no top line)
- Real-time preview in configuration menu

### ✓ Adjustable Magnifier Window
- Variable zoom levels (0.1x - 10x)
- Configurable capture radius and window size
- Adjustable refresh rate (10-60 FPS)
- Draggable magnified view window
- Smooth interpolation for quality scaling

### ✓ Optional Auto Gun-Detection
- Automatically shows overlays only when holding a firearm
- Keeps your screen clean when not in combat
- Configurable detection position for different screen resolutions

### ✓ Individual Overlay Controls
- Toggle crosshair independently
- Toggle magnifier independently
- Hide all overlays with a single key
- Fully customizable keybinds

### ✓ Configuration Menu
- User-friendly GUI for all settings
- Dark and light theme options
- Save/load configurations
- Reset to defaults option
- Real-time crosshair preview

### ✓ External & Safe
- Does not inject, hook, or modify any game files
- Functions like a standard accessibility overlay
- No game memory manipulation

---

## Controls

Default keybinds (fully customizable in config menu):

| Key | Action |
|-----|--------|
| **Up Arrow** | Toggle auto-detection for gun identification |
| **Down Arrow** | Exit the program |
| **Right Arrow** | Hide/show all overlays |
| **M** | Toggle magnifier overlay |
| **C** | Toggle crosshair overlay |

---

## Installation

1. Download or clone this repository

2. Ensure **Python 3.9+** is installed

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the configuration menu first (optional but recommended):
   ```bash
   python ViewFinder_Config_Menu.pyw
   ```

5. Run the main application:
   ```bash
   python ViewFinder_0.9.pyw
   ```

   Or simply double-click either `.pyw` file to run without a console window.

---

## Configuration

### First-Time Setup

1. Run `ViewFinder_Config_Menu.pyw`
2. Configure your preferred crosshair style, colors, and size
3. Set magnifier zoom level, capture radius, and window size
4. Adjust keybinds if desired
5. Click "Save Configuration"

### Recommended Settings

**For balanced performance:**
- Scale: 2.0x - 4.0x
- Radius: 50-100 pixels
- Window size: 300-500 pixels
- Refresh rate: 30-60 FPS

**For maximum zoom:**
- Scale: 8.0x - 10.0x
- Radius: 25-50 pixels (smaller radius = less lag)
- Window size: Match your desired display size
- Refresh rate: 30 FPS (higher rates may cause lag)

### Resolution-Specific Settings

The auto-detection position needs to be calibrated for your screen resolution:

**For 1920x1080:**
- Default detection position: [1718, 877]

**For other resolutions:**
1. Open the config menu
2. Navigate to "Options" → "Auto-Detection Settings"
3. Adjust X and Y positions to match your weapon indicator location
4. Test with auto-detection enabled

---

## Known Limitations

- The magnifier may experience frame drops at very high zoom levels (8x+) with large capture areas
- Auto-detection requires calibration for non-1080p resolutions
- Different screen resolutions require detection position adjustment
- High refresh rates (60 FPS) with large capture areas may impact performance

---

## Performance Tips

1. **Reduce capture radius** when using high zoom levels
2. **Lower refresh rate** to 30 FPS if experiencing lag
3. **Match window size** to magnified image size for best visual quality:
   - Formula: `window_size ≈ radius × 2 × scale`
   - Example: radius=50, scale=3.0 → window_size=300
4. **Close other applications** for best performance during gameplay

---

## File Structure

```
ViewFinder/
├── ViewFinder_0.9.pyw              # Main application
├── ViewFinder_Config_Menu.pyw      # Configuration GUI
├── crosshair_overlay.py            # Crosshair overlay logic
├── crosshair_config_widget.py      # Crosshair settings UI
├── crosshair_preview.py            # Crosshair preview widget
├── magnifier_overlay.py            # Magnifier overlay logic
├── magnifier_config_widget.py      # Magnifier settings UI
├── instructions_menu.py            # On-screen instructions display
├── overlay_toggles.py              # Overlay toggle management
├── viewfinder_config.json          # Saved configuration (generated)
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## Troubleshooting

**Overlays not appearing:**
- Check that the config file exists and is valid JSON
- Try resetting to defaults in the config menu
- Ensure no other overlay software is interfering

**Magnification not working:**
- Verify scale value is set correctly (2.0 or higher)
- Check that window size accommodates magnified image
- Try restarting the application

**Auto-detection not working:**
- Calibrate detection position for your resolution
- Ensure you're testing with a weapon equipped in-game
- Check console output for detection status messages

**Performance issues:**
- Lower refresh rate to 30 FPS
- Reduce capture radius
- Decrease zoom level
- Close background applications

---

## Future Improvements

- Per-game configuration profiles
- Dynamic magnifier positioning (follow cursor, anchor to crosshair)
- Additional crosshair styles and animations
- Hardware acceleration for better performance
- Multi-monitor support improvements
- Preset configurations for common use cases

---

## Credits

Developed for the BRM5 community to enhance helicopter gunner gameplay experience.

---

## License

MIT License — see `LICENSE` for details.

---

## Disclaimer

This is an external overlay tool that does not modify or interact with Roblox or BRM5 game files. It operates similarly to accessibility overlays and streaming software. Use at your own discretion.