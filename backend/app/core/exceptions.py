# Exceptions: 
# Exception is a built-in class in Python that is used to raise errors.
# Custom Exceptions: 
# AppException: Base exception for all custom exceptions in the application.
# Exceptions are used to handle errors in the application.
class AppException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# UserAlreadyExistsException: 
class UserAlreadyExistsException(AppException):
    pass

# InvalidCredentialsException: 
class InvalidCredentialsException(AppException):
    pass