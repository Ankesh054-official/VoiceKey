import psutil

def get_running_applications():
    apps = []
    for process in psutil.process_iter(['pid', 'name']):
        try:
            app_name = process.info['name']
            if app_name:  # Exclude processes with no name
                apps.append(app_name)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return apps

for i in get_running_applications():
    if "edge" in i.lower():
        print("Running Application:", i)
