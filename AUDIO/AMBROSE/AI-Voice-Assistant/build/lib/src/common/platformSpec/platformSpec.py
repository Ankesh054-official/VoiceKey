
from . import system, current_os

class PlatformSpecification:
    
    def __init__(self):
        self._OsType = ""
    
    def get_os_type(self):
        self._OsType = system()