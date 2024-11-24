import time
import logging
from application import Application, ApplicationNotFound

# Configure logging
logging.basicConfig(
    filename='application_test.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# List of applications to test
applications = [
    {"name": "whatsapp", "title": "WhatsApp"},
    {"name": "google chrome", "title": "Google Chrome"},
    {"name": "visual studio code", "title": "Visual Studio Code"},
    {"name": "vlc media player", "title": "VLC Media Player"},
    {"name": "notepad", "title": "Notepad"}
]

# Test all operations on applications
def test_application_operations(app_data):
    app_name = app_data["name"]
    app_title = app_data["title"]

    try:
        # Initialize the Application object
        app = Application(name=app_name)
        logging.info(f"Testing operations on {app_name}")

        # Launch the application
        app.launch()
        logging.info(f"{app_name} launched successfully.")
        time.sleep(2)  # Delay for visibility

        # Maximize the application window
        app.max(title=app_title)
        logging.info(f"{app_name} window maximized.")
        time.sleep(2)

        # Move the application window
        app.move([100, 50])
        logging.info(f"{app_name} window moved by offset [100, 50].")
        time.sleep(2)

        # Position the application window
        app.position("left-top")
        logging.info(f"{app_name} positioned to 'left-top' of the screen.")
        time.sleep(2)

        # Resize the application window
        app.resize([800, 600])
        logging.info(f"{app_name} resized to 800x600.")
        time.sleep(2)

        # Close the application
        app.close()
        logging.info(f"{app_name} closed successfully.")

    except ApplicationNotFound:
        logging.error(f"{app_name} not found on the system.")
    except Exception as e:
        logging.error(f"An error occurred while testing {app_name}: {e}")

# Run tests on each application
if __name__ == "__main__":
    for app_data in applications:
        test_application_operations(app_data)
        time.sleep(5)  # Delay between testing different applications for clarity
