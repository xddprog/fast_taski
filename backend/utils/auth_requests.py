from aiohttp import ClientSession
from fastapi import HTTPException

from backend.infrastructure.config.oauth_configs import VK_CONFIG, YANDEX_CONFIG


class AuthRequests:
    async def get_vk_access_token(self, code: str) -> str:
        async with ClientSession() as session:
            async with session.get(
                f"{VK_CONFIG.VK_BASE_URL}/oauth/access_token",
                params={
                    "client_id": VK_CONFIG.VK_CLIENT_ID,
                    "client_secret": VK_CONFIG.VK_CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": "https://www.fasttaski.ru/auth/callback",
                    "v": "5.131"
                },
                headers={"Accept": "application/json"},
                ssl=False
            ) as response:
                if response.status != 200:
                    print(await response.json())
                    raise HTTPException(status_code=400, detail="Во время авторизации произошла ошибка")
                response = await response.json()
                return response["access_token"], response["user_id"]
            
    async def get_vk_user(self, token: str, user_id: int) -> dict:
        async with ClientSession() as session:
            async with session.get(
                f"{VK_CONFIG.VK_API_URL}/users.get",
                params={
                    "user_ids": user_id,
                    "access_token": token,
                    "v": "5.131"
                },
                headers={"Accept": "application/json"},
                ssl=False
            ) as response:
                response = await response.json()
                return response["response"][0]
            
    async def get_yandex_user(self, access_token: str) -> dict:
        async with ClientSession() as session:
            async with session.get(
                f"{YANDEX_CONFIG.YANDEX_API_URL}",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"OAuth {access_token}"
                },
                ssl=False
            ) as response:
                return await response.json()