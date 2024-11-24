import psutil
import pygetwindow as gw
import win32process
import win32gui
import win32con


def get_hwnd_by_app_name(app_name):
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if app_name.lower() in process.info['name'].lower():
                pid = process.info['pid']
                print(f"Found PID: {pid} for application: {app_name}")

                windows = gw.getWindowsWithTitle("")
                for window in windows:
                    hwnd = window._hWnd
                    _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                    if found_pid == pid:
                        window.minimize()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return None


# Example usage
app_name = "pycharm"  # Replace with the name of the application you're looking for
hwnd = get_hwnd_by_app_name(app_name)
if hwnd:
    print(f"HWND for {app_name}: {hwnd}")
else:
    print(f"No window found for {app_name}")
