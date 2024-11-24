import pygetwindow as gw
from pynput.mouse import Button, Controller
import ctypes
import time

# Initialize the mouse controller
mouse = Controller()

def get_scaling_factor():
    """Get the scaling factor for the primary display."""
    hdc = ctypes.windll.user32.GetDC(0)  # Get device context for the screen
    dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # Get DPI scaling (LOGPIXELSX)
    ctypes.windll.user32.ReleaseDC(0, hdc)  # Release the device context
    return dpi / 96  # 96 DPI is the default scaling factor

def move_mouse_to_window(title):
    """Move the mouse to the top-left corner of the window after adjusting for scaling."""
    # Get the window object
    window = gw.getWindowsWithTitle(title)
    if not window:
        print(f"Window with title '{title}' not found.")
        return

    window = window[0]  # Take the first match if multiple windows are found
    window.activate()
    # Get the window's left and top positions
    left, top = window.left, window.top

    # Get the scaling factor
    scaling_factor = get_scaling_factor()
    print(scaling_factor)

    # Adjust the coordinates for scaling
    adjusted_left = int(left * scaling_factor)
    adjusted_top = int(top * scaling_factor)

    # Move the mouse to the adjusted coordinates using pynput
    mouse.position = (adjusted_left+20, adjusted_top+15)
    time.sleep(2)
    mouse.press(Button.left)
    time.sleep(2)
    mouse.position = (2750 - 70, 100)
    mouse.release(Button.left)
    print(f"Mouse moved to: {adjusted_left}px, {adjusted_top}px (adjusted for scaling)")

# Example usage
move_mouse_to_window("whatsapp")
