
from fastapi import HTTPException

class DigioDataNotFound(HTTPException):
    def __init__(self, message="Data was not found."):
        super().__init__(status_code=422,detail=message)
        
class FilterKeyNotPresent(HTTPException):
    def __init__(self, message="Key provided does not exists."):
        super().__init__(status_code=422,detail=message)


class ValidationError(HTTPException):
    def __init__(self, message="Something went wrong."):
        super().__init__(status_code=422, detail=message)

class MultipleRecordFoundError(HTTPException):
    def __init__(self, message="Expecting 1 but queryset return multiple records"):
        super().__init__(status_code=422,detail=message)

class DoesNotExistException(HTTPException):
    def __init__(self, message='Object does not exist'):
        super().__init__(status_code=400, detail=message)

class ConflictException(HTTPException):
    def __init__(self, message='Conflict'):
        super().__init__(status_code=422,detail=message)


class UnauthorizedException(HTTPException):
    def __init__(self, message='User is not authorized'):
        super().__init__(status_code=403, detail=message)


class CredentialException(HTTPException):
    def __init__(self, message='Could not validate credentials.Username/password is incorrect'):
        super().__init__(status_code=401,headers={"WWW-Authenticate": "Bearer"}, detail=message)





