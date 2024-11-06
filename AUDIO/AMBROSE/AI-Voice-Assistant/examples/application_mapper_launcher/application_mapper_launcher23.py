import os
import subprocess
import winreg

class Application:
    def __init__(self, name, path, is_store_app=False, app_id=None):
        self.name = name
        self.path = path
        self.is_store_app = is_store_app
        self.app_id = app_id  # Microsoft Store AppId

    def launch(self):
        """Launch the application, dynamically handling Microsoft Store and system apps."""
        try:
            if os.path.exists(self.path):
                # Use os.startfile for executables with valid paths
                os.startfile(self.path)
            elif self.is_store_app and self.app_id:
                # For Microsoft Store apps, use shell:appsFolder with AppId
                print(f"Launching {self.name} via appsFolder URI...")
                subprocess.run(f"explorer.exe shell:appsFolder\\{self.app_id}", shell=True)
            else:
                # For unknown applications, try with a URI format
                print(f"Launching {self.name} with fallback URI...")
                subprocess.run(["explorer.exe", f"ms-{self.name.lower()}:"])
            print(f"Launching {self.name}...")
        except FileNotFoundError:
            print(f"Application {self.name} not found at path {self.path}")
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

    def fetch_microsoft_store_apps(self):
        """Fetch Microsoft Store apps using PowerShell."""
        try:
            result = subprocess.run(
                ["powershell", "-Command", "Get-AppxPackage | Select-Object Name, PackageFullName, InstallLocation"],
                capture_output=True, text=True, shell=True
            )
            if result.returncode == 0:
                output_lines = result.stdout.splitlines()
                for line in output_lines[3:]:  # Skip headers
                    parts = line.split()
                    if len(parts) >= 3:
                        app_name = parts[0]
                        package_name = parts[1]
                        app_id = parts[2]
                        # Store path using full package name for the Store app
                        self.apps.append(Application(app_name, app_id, is_store_app=True, app_id=app_id))
            else:
                print("Failed to retrieve Microsoft Store apps:", result.stderr)
        except Exception as e:
            print(f"Error fetching Microsoft Store apps: {e}")

    def dynamic_search_apps(self):
        """Search for application executables in common directories."""
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
        """Aggregate all applications by fetching from registry, Microsoft Store, and common directories."""
        self.fetch_registry_apps()
        self.fetch_microsoft_store_apps()
        self.dynamic_search_apps()

    def search_app(self, app_name):
        """Search for an application by name."""
        found_apps = []
        for app in self.apps:
            if app_name.lower() in app.name.lower() or app_name.lower() in app.path.lower():
                found_apps.append(app)

        # If no apps are found by name, also try searching for related apps in the registry and store apps
        if not found_apps:
            print(f"Trying to search for '{app_name}' in installed apps...")
            for app in self.apps:
                if app_name.lower() in app.name.lower() or app_name.lower() in app.path.lower():
                    found_apps.append(app)

        return found_apps if found_apps else None

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
