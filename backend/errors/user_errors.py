from fastapi import HTTPException


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail='User not found')