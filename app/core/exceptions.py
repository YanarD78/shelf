class AppError(Exception):
    status_code = 500
    detail = "Internal server error"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)



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



class ExternalServerError(AppError):
    status_code = 502
    detail = "External server is unavailable"



class ItemNotFound(AppError):
    status_code = 404
    detail = "Item not found"

class RecordAlreadyExists(AppError):
    status_code = 409
    detail = "Record already exists"