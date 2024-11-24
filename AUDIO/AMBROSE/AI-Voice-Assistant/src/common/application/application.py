import logging
import psutil
import pygetwindow as gw
import win32con
import win32gui
import win32process
import ctypes
import time

from pynput.mouse import Button, Controller
from AppOpener import open, features
from ApplicationException import ApplicationNotFound


class ApplicationUtils:
    """
    A utility class for interacting with application windows on the desktop.

    This class provides methods to retrieve information about open windows,
    such as their titles, dimensions, positions, and states.
    """

    def __init__(self):
        """
        Initialize the ApplicationUtils instance.
        """
        pass

    def __get_all_window_title(self):
        """
        Get the titles of all currently opened windows.

        Returns:
            list[str]: A list of strings representing the titles of all open windows.
        """
        return gw.getAllTitles()

    def __get_all_windows(self):
        """
        Get objects representing all currently opened windows.

        Returns:
            list[pygetwindow.window.Window]: A list of Window objects for all open windows.
        """
        return gw.getAllWindows()

    def __get_windows_with_title(self, title=""):
        """
        Get the windows with titles containing the specified application name.

        Args:
            app_name (str): The name of the application to search for.

        Returns:
            list[pygetwindow.window.Window]: A list of windows matching the specified title.
        """
        return gw.getWindowsWithTitle(title=title)

    def __get_active_windows(self):
        """
        Get the currently active window.

        Returns:
            pygetwindow.window.Window: The Window object representing the active window.
        """
        return gw.getActiveWindow()

    def __get_window_at(self, x: int, y: int):
        """
        Get the window at a specified screen position.

        Args:
            x (int): The X-coordinate on the screen.
            y (int): The Y-coordinate on the screen.

        Returns:
            pygetwindow.window.Window or None: The Window object at the specified position, or None if no window is found.
        """
        return gw.getWindowsAt(x, y)

    def __get_title_of_win_by_hWnd(self, hWnd):
        """
        Get the title of a window given its handle (hWnd).

        Args:
            hWnd (int): The handle of the window.

        Returns:
            str: The title of the window.
        """
        return win32gui.GetWindowText(hWnd)

    def getTitleByHWND(self, hWnd):
        """
        Public method to retrieve the title of a window given its handle (hWnd).

        Args:
            hWnd (int): The handle of the window.

        Returns:
            str: The title of the window.
        """
        return self.__get_title_of_win_by_hWnd(hWnd)

    def getWindowsWithTitle(self, title=""):
        """
        Public method to retrieve windows with a specific title.

        Args:
            title (str): The title of the window to search for.

        Returns:
            list[pygetwindow.window.Window]: A list of windows with the matching title.
        """
        return self.__get_windows_with_title(title=title)

    def getAllWindowTitle(self):
        """
        Public method to get the titles of all currently opened windows.

        Returns:
            list[str]: A list of window titles.
        """
        return self.__get_all_window_title()

    def getAllWindows(self):
        """
        Public method to get all currently opened windows.

        Returns:
            list[pygetwindow.window.Window]: A list of Window objects for all open windows.
        """
        return self.__get_all_windows()

    def getActiveWindows(self):
        """
        Public method to get the currently active window.

        Returns:
            pygetwindow.window.Window: The active Window object.
        """
        return self.__get_active_windows()


class Application(ApplicationUtils):
    """
    A class for managing and controlling application windows.

    This class extends ApplicationUtils to provide functionalities for
    launching, resizing, moving, minimizing, and maximizing application windows.
    """

    def __init__(self, name=""):
        """
        Initialize the Application instance.

        Args:
            name (str): The name of the application to manage.
        """
        super().__init__()
        self.name = name.lower()
        self.mouse = Controller()

        self.obj = None
        logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(threadName)s] %(message)s')

    def __get_hwnd_by_app_name(self, app_name=""):
        """
        Get window handles of a specific application by name.

        Args:
            app_name (str): The name of the application.

        Returns:
            list[tuple]: A list of tuples containing the window handle and title.
        """
        for process in psutil.process_iter(attrs=['pid', 'name']):
            try:
                if app_name.lower() in process.info['name'].lower():
                    pid = process.info['pid']

                    windows = gw.getAllWindows()
                    for window in windows:
                        hwnd = window._hWnd
                        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                        if found_pid == pid or app_name.lower() in window.title.lower():
                            return window
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                logging.error(f"{process.info['pid']}, {process.info['name']}")
        return None

    def get_window_hwnd(self, app_name="", title=""):
        """
        Get the window handle based on application name or title.

        Args:
            app_name (str): The name of the application.
            title (str): The title of the application window.

        Returns:
            list[tuple]: A list of window handles and titles.
        """
        __window = []

        if app_name and not title:
            __window = self.__get_hwnd_by_app_name(app_name=app_name)
            print(f"step 3, {app_name} get_window_hwnd",__window)

        if not app_name and title:
            try:
                for __win in self.getWindowsWithTitle(title=title):
                    __window.append((__win._hWnd, __win.title.lower()))
            except IndexError:
                raise ApplicationNotFound(f"'{app_name or title}' is not open, Opening it.")

        return __window

    def is_active(self, window_title:str):
        """
        Checks if a window with the given title is currently active (in the foreground).

        Args:
        - window_title (str): The title of the window to check.

        Returns:
        - bool: True if the window is active, False otherwise.
        """
        try:
            # Get the currently active window's title
            active_window = gw.getActiveWindow()

            # Compare the active window's title with the given window title
            if active_window and window_title.lower() in active_window.title.lower():
                return True
            return False
        except Exception as e:
            logging.error(f"Error: {e}")
            return False

    def launch(self):
        """
        Launch the application.

        Raises:
            ApplicationNotFound: If the application is not found.

        Returns:
            list[pygetwindow.window.Window]: A list of windows for the launched application.
        """
        try:
            install = True
            for i in self.getAllWindows():
                if i.title.lower() == self.name:
                    install = False
            if install:
                open(self.name, match_closest=True, throw_error=True)
            self.obj = self.getWindowsWithTitle(self.name)
            return self.obj

        except features.AppNotFound:
            raise ApplicationNotFound(f"Required application '{self.name}' not found")

    def destroy(self):
        """
        Close the application window.
        """

        try:
            logging.info(f"Closing window {self.name}")
            win32gui.PostMessage(self.getWindowsWithTitle(self.name)[0]._hWnd, win32con.WM_CLOSE, 0, 0)
        except IndexError:
            logging.info(f"{self.name} window already closed.")

    def resize(self, size: list[int, int]):
        """
        Resize the application window to the specified size.

        Parameters:
            size (list[int, int]): A list of two integers specifying the new width and height of the window.

        Raises:
            TypeError: If `size` is not a list of two integers.

        Example:
            resize([800, 600])
        """

        if not isinstance(size, list):
            raise TypeError("size must be list of int: [int, int]")

        if len(size) != 2:
            raise TypeError("size can only contain two elements")

        __windows = self.get_window_hwnd(title=self.name)
        for __win in __windows:
            if self.name == __win[1]:
                self.getWindowsWithTitle(__win[1])[0].resize(size[0], size[1])

    def resizeTo(self, size: list[int, int]):
        """
        Resize the application window to the exact specified size.

        Parameters:
            size (list[int, int]): A list of two integers specifying the exact width and height.

        Raises:
            TypeError: If `size` is not a list of two integers.

        Example:
            resizeTo([1024, 768])
        """

        if not isinstance(size, list):
            raise TypeError("size must be tuple of int: [int, int]")

        if len(size) != 2:
            raise TypeError("size can only contain two elements")

        __windows = self.get_window_hwnd(title=self.name)
        for __win in __windows:
            if self.name == __win[1]:
                self.getWindowsWithTitle(__win[1])[0].resizeTo(size[0], size[1])

    def move(self, value: list[int, int]):
        """
        Move the application window by a specified offset.

        Parameters:
            value (list[int, int]): A list of two integers representing the x and y offset.

        Raises:
            TypeError: If `value` is not a list of two integers.

        Example:
            move([100, 50])
        """

        if not isinstance(value, list):
            raise TypeError("value must be list of int: [int, int]")

        if len(value) != 2:
            raise TypeError("value can only contain two elements")

        __windows = self.get_window_hwnd(title=self.name)
        for __win in __windows:
            if self.name == __win[1]:
                self.getWindowsWithTitle(__win[1])[0].move(value[0], value[1])

    def move_to(self, value: list[int, int]):
        """
        Move the application window to the specified coordinates.

        Parameters:
            value (list[int, int]): A list of two integers specifying the target x and y coordinates.

        Raises:
            TypeError: If `value` is not a list of two integers.

        Example:
            move_to([500, 300])
        """

        if not isinstance(value, list):
            raise TypeError("value must be tuple of int: [int, int]")

        if len(value) != 2:
            raise TypeError("value can only contain two elements")

        __windows = self.get_window_hwnd(title=self.name)
        for __win in __windows:
            if self.name == __win[1]:
                print(self.getWindowsWithTitle(__win[1])[0])
                self.getWindowsWithTitle(__win[1])[0].moveTo(value[0], value[1])

    def get_scaling_factor(self):
        """
        Get the DPI scaling factor for the primary display.

        Returns:
            float: The scaling factor relative to the default 96 DPI.

        Example:
            scaling_factor = get_scaling_factor()
            print(scaling_factor)
        """
        hdc = ctypes.windll.user32.GetDC(0)  # Get device context for the screen
        dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # Get DPI scaling (LOGPIXELSX)
        ctypes.windll.user32.ReleaseDC(0, hdc)  # Release the device context
        return dpi / 96  # 96 DPI is the default scaling factor

    def position(self, pos=""):
        """
        Position the application window in predefined layouts on the screen.

        Parameters:
            pos (str): The desired layout position (e.g., "center", "left-top", "right-bottom").

        Layout Options:
            - "center-top": Align at the top center of the screen.
            - "center-justified": Align in the center of the screen.
            - "center-bottom": Align at the bottom center of the screen.
            - "left-top", "left-justified", "left-bottom", "left": Left-side layouts.
            - "right-top", "right-justified", "right-bottom", "right": Right-side layouts.

        Raises:
            KeyError: If the provided position is invalid.

        Example:
            position("center")
        """

        max_left_value, max_top_value = 2757, 1675
        max_height, max_width = 1096, 1936
        min_height, min_width = 509, 516
        def ct(obj):
            obj.height = int(max_height/2)
            obj.width = int(max_width/3)
            obj.left = int(max_width/3)
            obj.top = 0

        def cj(obj):
            obj.height = int(max_height / 3)
            obj.width = int(max_width / 3)
            obj.left = int(max_width / 3)
            obj.top = int(max_height/3)

        def cb(obj):
            obj.height = int(max_height / 2)
            obj.width = int(max_width / 3)
            obj.left = int(max_width / 3)
            obj.top = int(max_height-obj.height)

        def c(obj):
            obj.height = max_height
            obj.width = int(max_width / 3)
            obj.left = int(max_width / 3)
            obj.top = 0

        def lt(init_mouse_pos):
            self.mouse.position = init_mouse_pos
            self.mouse.press(Button.left)
            self.mouse.release(Button.left)
            self.mouse.press(Button.left)
            time.sleep(0.8)
            self.mouse.position = (0, 100)
            self.mouse.release(Button.left)

        def lj(obj):
            obj.height = int(max_height / 4)
            obj.width = int(max_width / 3)
            obj.left = 0
            obj.top = int(obj.height / 2)

        def lb(init_mouse_pos):
            self.mouse.position = init_mouse_pos
            self.mouse.press(Button.left)
            self.mouse.release(Button.left)
            self.mouse.press(Button.left)
            time.sleep(0.8)
            self.mouse.position = (0, max_top_value-500)
            self.mouse.release(Button.left)

        def l(init_mouse_pos):
            self.mouse.position = init_mouse_pos
            self.mouse.press(Button.left)
            self.mouse.release(Button.left)
            self.mouse.press(Button.left)
            time.sleep(0.8)
            self.mouse.position = (0, int(max_height/2))
            self.mouse.release(Button.left)

        def rt(init_mouse_pos):
            self.mouse.position = init_mouse_pos
            self.mouse.press(Button.left)
            self.mouse.release(Button.left)
            self.mouse.press(Button.left)
            time.sleep(0.8)
            self.mouse.position = (max_left_value - 70, 100)
            self.mouse.release(Button.left)

        def rj(obj):
            obj.height = int(max_height / 4)
            obj.width = int(max_width / 3)
            obj.left = int(max_width - obj.width)
            obj.top = int(obj.height / 2)

        def rb(init_mouse_pos):
            self.mouse.position = init_mouse_pos
            self.mouse.press(Button.left)
            self.mouse.release(Button.left)
            self.mouse.press(Button.left)
            time.sleep(0.8)
            self.mouse.position = (max_left_value-70, max_top_value-500)
            self.mouse.release(Button.left)

        def r(init_mouse_pos):
            self.mouse.position = init_mouse_pos
            self.mouse.press(Button.left)
            self.mouse.release(Button.left)
            self.mouse.press(Button.left)
            time.sleep(0.8)
            self.mouse.position = (max_width, 500)
            self.mouse.release(Button.left)

        __window = None

        while True if __window is None else False:
            try:
                __window = self.getWindowsWithTitle(self.name)[0]
            except IndexError:
                pass

        left, top, title = __window.left, __window.top, __window.title
        scaling_factor = self.get_scaling_factor()

        adjusted_left, adjusted_top = int(left * scaling_factor), int(top * scaling_factor)
        self.switch(__window)
        __win_position = (adjusted_left + 100, adjusted_top + 15)
        args = {
                "pos":__win_position,
                "obj":__window
                }

        operation = {
        "center-top": lambda x: ct(x["obj"]),
        "center-justified": lambda x: cj(x["obj"]),
        "center-bottom": lambda x: cb(x["obj"]),
        "center": lambda x: c(x["obj"]),
        "left-top": lambda x: lt(x["pos"]),
        "left-justified": lambda x: lj(x["obj"]),
        "left-bottom": lambda x: lb(x["pos"]),
        "left": lambda x: l(x["pos"]),
        "right-top": lambda x: rt(x["pos"]),
        "right-justified": lambda x: rj(x["obj"]),
        "right-bottom": lambda x: rb(x["pos"]),
        "right": lambda x: r(x["pos"])
        }

        if pos in operation.keys():
            operation[pos](args)
        else:
            raise KeyError(f"Provided position is invalid '{pos}'")

    def min(self, title=""):
        """
        Minimize the application window.

        Parameters:
            title (str): The title of the window to minimize. If not provided, the current application's title is used.

        Logs:
            - Info: When a window is successfully minimized.
            - Error: When no matching window is found or the application is not installed.

        Example:
            min("MyApp")
        """

        __window = None

        if not title:
            app_name = self.name
            __window = self.__get_hwnd_by_app_name(app_name=app_name)

        if title:
            for __app in self.getAllWindows():
                if title.lower() in __app.title.lower():
                    __window = __app
                    break

        __window.minimize()
        __window.activate()

    def max(self, title=""):
        """
        Maximize the application window.

        Parameters:
            title (str): The title of the window to maximize. If not provided, the current application's title is used.

        Logs:
            - Info: When a window is successfully maximized.
            - Error: When no matching window is found or the application is not installed.

        Example:
            max("MyApp")
        """

        __window = None

        if not title:
            app_name = self.name
            __window = self.__get_hwnd_by_app_name(app_name=app_name)

        if title:
            for __app in self.getAllWindows():
                if title.lower() in __app.title.lower():
                    __window = __app
                    break
        __window.maximize()
        __window.activate()

    def switch(self, obj=None, title="", appname=""):
        """
        Switch focus to the application with the specified title.

        Parameters:
            title (str): The title of the application to switch to.

        Behavior:
            - Activates the window if found.
            - Launches the application if not already running.

        Raises:
            ApplicationNotFound: If the application is not installed or cannot be launched.

        Example:
            switch("Calculator")
        """
        __window = None

        if obj is not None:
            __window = obj

        if title:
            for __app in self.getAllWindows():
                if title.lower() in __app.title.lower():
                    __window = __app
                    break

        if appname:
            __window = self.__get_hwnd_by_app_name(app_name=appname)

        if __window is not None:
            __window.activate()
        else:
            self.obj[0].activate()