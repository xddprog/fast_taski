from fastapi import HTTPException


class ColumnNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail='Колонка не найдена')


class ColumnAlreadyExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='Колонка с таким именем уже существует')