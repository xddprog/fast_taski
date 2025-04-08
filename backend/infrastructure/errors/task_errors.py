from fastapi import HTTPException


class TaskNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Задача не найдена")
        