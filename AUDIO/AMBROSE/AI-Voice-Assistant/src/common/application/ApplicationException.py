
class ApplicatonException(Exception):
    pass

class ApplicationNotFound(ApplicatonException):
     def __init__(self, message):
         self.message = message
         ApplicatonException(self.message)
