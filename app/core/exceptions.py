class AppError(Exception):
    status_code = 500
    detail = "Internal server error"



class UserAlreadyExistsError(AppError):
    status_code = 409
    detail = "User with this username or email already exists"

class InvalidCredentialsError(AppError):
    status_code = 401
    detail = "Incorrect username or password"



class TokenExpiredError(AppError):
    status_code = 401
    detail = "The token has expired"

class InvalidTokenError(AppError):
    status_code = 401
    detail = "Could not validate credentials"