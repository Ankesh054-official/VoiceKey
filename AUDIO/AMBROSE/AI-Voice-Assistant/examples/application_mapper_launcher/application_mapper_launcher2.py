import subprocess
import winreg
import os

class Application:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def launch(self):
        try:
            if self.path.startswith("shell:AppsFolder"):
                subprocess.Popen(["explorer.exe", self.path], shell=True)
            else:
                subprocess.Popen([self.path], shell=True)
            print(f"Launching {self.name}...")
        except Exception as e:
            print(f"Failed to launch {self.name}: {e}")


class InstalledApplications:
    def __init__(self):
        self.apps = []

    def fetch_registry_apps(self):
        """Fetches installed applications from Windows registry."""
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
                                    self.apps.append(Application(app_name, install_location))
                        except (FileNotFoundError, OSError):
                            pass
            except Exception as e:
                print(f"Error accessing registry path {path}: {e}")

    def fetch_microsoft_store_apps(self):
        """Fetches Microsoft Store apps using PowerShell."""
        try:
            result = subprocess.run(
                ["powershell", "-Command", "Get-AppxPackage | Select-Object Name, PackageFullName"],
                capture_output=True, text=True, shell=True
            )
            if result.returncode == 0:
                output_lines = result.stdout.splitlines()
                for line in output_lines[3:]:  # Skip headers
                    parts = line.split()
                    if len(parts) >= 2:
                        app_name = parts[0]
                        package_name = parts[1]
                        store_path = f"shell:AppsFolder\\{package_name}"
                        self.apps.append(Application(app_name, store_path))
            else:
                print("Failed to retrieve Microsoft Store apps:", result.stderr)
        except Exception as e:
            print(f"Error fetching Microsoft Store apps: {e}")

    def fetch_custom_app_paths(self):
        """Automatically searches for VS Code, IntelliJ IDEA, and Android Studio paths."""
        app_paths = {
            "Visual Studio Code": [
                r"C:\Program Files\Microsoft VS Code\Code.exe",
                r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            ],
            "IntelliJ IDEA": [
                r"C:\Program Files\JetBrains\IntelliJ IDEA\bin\idea64.exe",
                r"C:\Program Files (x86)\JetBrains\IntelliJ IDEA\bin\idea64.exe"
            ],
            "Android Studio": [
                r"C:\Program Files\Android\Android Studio\bin\studio64.exe",
                r"C:\Program Files (x86)\Android\Android Studio\bin\studio64.exe"
            ]
        }
        for app_name, paths in app_paths.items():
            for path in paths:
                expanded_path = os.path.expandvars(path)
                if os.path.exists(expanded_path):
                    self.apps.append(Application(app_name, expanded_path))
                    break  # Stop after finding the first valid path

    def get_all_apps(self):
        """Aggregates all applications by fetching from registry, Microsoft Store, and custom paths."""
        self.fetch_registry_apps()
        self.fetch_microsoft_store_apps()
        self.fetch_custom_app_paths()

    def search_app(self, app_name):
        """Searches for an application by name."""
        for app in self.apps:
            if app_name.lower() in app.name.lower():
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
