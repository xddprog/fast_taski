from fastapi import HTTPException


class TagNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Тег не найден",
        )