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


class UserNotFoundRights(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="У вас нет доступа к изменениям данной команды!",
        )


class UserNotInTeam(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Вы не состоите в этой команде!",
        )


class UserAlreadyInTeam(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Вы уже состоите в этой команде!",
        )


class InvalidInviteToken(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Неверный токен приглашения!",
        )