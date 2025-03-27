from fastapi import HTTPException


class TeamAlreadyExist(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Команда с таким именем уже существует!",
        )
    

class TeamNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Команда не найдена!",
        )