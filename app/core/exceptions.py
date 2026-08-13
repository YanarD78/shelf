class AppError(Exception):
    status_code = 500
    detail = "Internal server error"

class UserAlreadyExistsError(AppError):
    status_code = 409
    detail = "User with this username or email already exists"

class InvalidCredentialsError(AppError):
    status_code = 401
    detail = "Incorrect username or password"