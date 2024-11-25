import psutil
import win32gui
import win32process

# Get PIDs of a specific application (e.g., "notepad.exe")
target_pids = [proc.pid for proc in psutil.process_iter(['name']) if proc.info['name'] == 'pycharm64.exe']

# Callback to find windows of the target PIDs
def enum_windows(hwnd, results):
    if win32gui.IsWindowVisible(hwnd):
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        if pid in target_pids:
            results.append((hwnd, win32gui.GetWindowText(hwnd)))

results = []
win32gui.EnumWindows(enum_windows, results)

# Print results
for hwnd, title in results:
    print(f"Window Handle: {hwnd}, Title: {title}")