import os
import winreg

class Application:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def launch(self):
        """Launch the application using os.startfile()."""
        try:
            os.startfile(self.path)
            print(f"Launching {self.name}...")
        except Exception as e:
            print(f"Failed to launch {self.name}: {e}")


class InstalledApplications:
    def __init__(self):
        self.apps = []

    def fetch_registry_apps(self):
        """Fetch installed applications from Windows registry."""
        uninstall_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        for path in uninstall_paths:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                app_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                if app_name and install_location:
                                    exe_path = os.path.join(install_location, f"{app_name}.exe")
                                    if os.path.exists(exe_path):  # Verify the path exists
                                        self.apps.append(Application(app_name, exe_path))
                        except (FileNotFoundError, OSError, IndexError):
                            pass
            except Exception as e:
                print(f"Error accessing registry path {path}: {e}")

    def dynamic_search_apps(self):
        """Search for known application executables in common directories."""
        search_paths = [
            os.environ.get("ProgramFiles"),
            os.environ.get("ProgramFiles(x86)"),
            os.path.expandvars(r"%LOCALAPPDATA%")
        ]
        app_files = {
            "Visual Studio Code": "Code.exe",
            "IntelliJ IDEA": ["idea64.exe", "idea.exe"],
            "Android Studio": "studio64.exe"
        }

        for search_path in search_paths:
            if search_path and os.path.exists(search_path):
                for root, _, files in os.walk(search_path):
                    for app_name, executables in app_files.items():
                        if isinstance(executables, str):
                            executables = [executables]
                        for exe in executables:
                            if exe in files:
                                app_path = os.path.join(root, exe)
                                if os.path.exists(app_path):  # Verify the path exists
                                    self.apps.append(Application(app_name, app_path))
                                    print(f"Found {app_name} at {app_path}")
                                    break  # Stop if we found an app match

    def get_all_apps(self):
        """Aggregate all applications by fetching from registry and common directories."""
        self.fetch_registry_apps()
        self.dynamic_search_apps()

    def search_app(self, app_name):
        """Search for an application by name."""
        for app in self.apps:
            if (app_name.lower() in app.path.lower()) or (app_name.lower() in app.name.lower()):
                return app
        return None

    def list_apps(self):
        """Lists all applications."""
        for app in self.apps:
            print(f"{app.name} - Path: {app.path}")


class ApplicationLauncher:
    def __init__(self):
        self.installed_apps = InstalledApplications()
        self.installed_apps.get_all_apps()

    def launch_app_by_name(self, app_name):
        """Launches an application by its name."""
        app = self.installed_apps.search_app(app_name)
        if app:
            app.launch()
        else:
            print(f"Application '{app_name}' not found.")


# Example usage
if __name__ == "__main__":
    launcher = ApplicationLauncher()
    launcher.installed_apps.list_apps()  # List all installed applications

    # Launch a specific application by name
    app_to_launch = input("Enter the name of the application to launch: ")
    launcher.launch_app_by_name(app_to_launch)
