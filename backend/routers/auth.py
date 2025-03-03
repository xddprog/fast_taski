from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response

from backend.core.clients.smtp_clients import SMTPClients
from backend.core.enums import AuthServices, EmailServices
from backend.dto.auth_dto import ExternalServiceUserData, RegisterForm, LoginForm
from backend.dto.user_dto import BaseUserModel
from backend.services import AuthService
from backend.core.dependencies import (
    get_auth_service,
    get_current_user_dependency,
    get_smtp_clients,
    get_tfa_service,
)
from backend.services.tfa_service import TwoFactorAuthService
from backend.utils.auth_requests import AuthRequests


router = APIRouter()


async def set_cookie_tokens(access_token: str, refresh_token: str, response: Response):
    response.set_cookie(key="access_token", value=access_token)
    response.set_cookie(key="refresh_token", value=refresh_token)


@router.get("/current_user")
async def get_current_user(
    current_user: BaseUserModel = Depends(get_current_user_dependency),
) -> BaseUserModel:
    return current_user


@router.post("/check-exist")
async def check_user_in_app(
    userForm: RegisterForm | LoginForm,
    is_register: bool,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    two_factor_service: Annotated[TwoFactorAuthService, Depends(get_tfa_service)],
    smtp_clients: Annotated[SMTPClients, Depends(get_smtp_clients)],
    background_tasks: BackgroundTasks
) -> None:
    username = await auth_service.check_user_in_app(userForm, is_register)
    code = await two_factor_service.generate_code(
        userForm.username if is_register else username
    )
    await smtp_clients.send_verification_code(
        userForm.email,
        code,
        userForm.username if is_register else username,
        background_tasks
    )


@router.post("/login")
async def login_user(
    form: LoginForm,
    response: Response,
    code: str,
    two_factor_service: Annotated[TwoFactorAuthService, Depends(get_tfa_service)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> BaseUserModel:
    user = await auth_service.get_user_by_email(form.email)

    await two_factor_service.check_code(user.username, code)

    access_token = await auth_service.create_access_token(user.username)
    refresh_token = await auth_service.create_refresh_token(user.username)
    await set_cookie_tokens(access_token, refresh_token, response)
    return user


@router.post("/refresh")
async def refresh_token(
    request: Request, 
    response: Response,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    refresh_token = request.cookies.get("refresh_token")
    email = await auth_service.verify_token(refresh_token)
    access_token = await auth_service.create_access_token(email)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    

@router.delete("/logout")
async def logout_user(response: Response) -> dict[str, str]:
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"detail": "Вы вышли из аккаунта"}


@router.post("/register", status_code=201)
async def register_user(
    form: RegisterForm,
    code: str,
    response: Response,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    two_factor_service: Annotated[TwoFactorAuthService, Depends(get_tfa_service)],
) -> BaseUserModel:
    await two_factor_service.check_code(form.username, code)
    
    new_user = await auth_service.register_user(form)
    access_token = await auth_service.create_access_token(form.email)
    refresh_token = await auth_service.create_refresh_token(form.email)
    await set_cookie_tokens(access_token, refresh_token, response)
    return new_user


@router.post("/github")
async def login_with_github(
    code: str, 
    auth_requests: Annotated[AuthRequests, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    response: Response
) -> BaseUserModel:
    token = await auth_requests.get_github_access_token(code)
    user = await auth_requests.get_github_user(token)
    user = await auth_service.auth_github_user(
        ExternalServiceUserData(
            username=user["login"],
            email=user["email"],
            external_id=user["id"],
            service=AuthServices.GITHUB.value,
        )
    )
    access_token = await auth_service.create_access_token(user.username)
    refresh_token = await auth_service.create_refresh_token(user.username)

    await set_cookie_tokens(access_token, refresh_token, response)
    return user


@router.post("/vk")
async def login_with_vk(
    code: str, 
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    auth_requests: Annotated[AuthRequests, Depends()],
    response: Response
):
    token, user_id = await auth_requests.get_vk_access_token(code)
    user = await auth_requests.get_vk_user(token, user_id)

    user = await auth_service.auth_extarnal_service_user(
        ExternalServiceUserData(
            username=f"{user["first_name"]} {user['last_name']}",
            external_id=user["id"],
            service=AuthServices.VK.value,
        )
    )
    access_token = await auth_service.create_access_token(user.username)
    refresh_token = await auth_service.create_refresh_token(user.username)

    await set_cookie_tokens(access_token, refresh_token, response)
    return user


@router.post("/yandex")
async def login_with_yandex(
    access_token: str, 
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    auth_requests: Annotated[AuthRequests, Depends()],
    response: Response
):
    user = await auth_requests.get_yandex_user(access_token)
    user = await auth_service.auth_extarnal_service_user(
        ExternalServiceUserData(
            username=user["display_name"],
            email=user["default_email"],
            external_id=user["id"],
            service=AuthServices.YANDEX.value,
        )
    )

    access_token = await auth_service.create_access_token(user.username)
    refresh_token = await auth_service.create_refresh_token(user.username)
    await set_cookie_tokens(access_token, refresh_token, response)
    return user


@router.post("/telegram")
async def login_with_telegram(
    code: str, 
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    auth_requests: Annotated[AuthRequests, Depends()],
    response: Response
):
    pass