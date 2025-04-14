from fastapi import HTTPException


class NoteNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Заметка не найдена")