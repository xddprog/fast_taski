from aiohttp import ClientSession

from backend.core.config.oauth_configs import load_github_config, load_vk_config, load_yandex_config


class AuthRequests:
    def __init__(self):
        self.github_config = load_github_config()
        self.vk_config = load_vk_config()
        self.yandex_config = load_yandex_config()

    async def get_github_access_token(self, code: str) -> str:
        async with ClientSession() as session:
            async with session.get(
                f"{self.github_config.GITHUB_BASE_URL}/login/oauth/access_token",
                params={
                    "client_id": self.github_config.GITHUB_CLIENT_ID,
                    "client_secret": self.github_config.GITHUB_CLIENT_SECRET,
                    "code": code
                },
                headers={"Accept": "application/vnd.github+json"},
                ssl=False
            ) as response:
                response = await response.json()
                return response["access_token"]
            
    async def get_github_user(self, token: str) -> dict:
        async with ClientSession() as session:
            async with session.get(
                f"{self.github_config.GITHUB_API_URL}/user", 
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json"
                },
                ssl=False
            ) as response:
                return await response.json()
            
    async def get_vk_access_token(self, code: str) -> str:
        async with ClientSession() as session:
            async with session.get(
                f"{self.vk_config.VK_BASE_URL}/oauth/access_token",
                params={
                    "client_id": self.vk_config.VK_CLIENT_ID,
                    "client_secret": self.vk_config.VK_CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": "https://d6af-176-124-206-69.ngrok-free.app/auth/callback",
                    "v": "5.131"
                },
                headers={"Accept": "application/json"},
                ssl=False
            ) as response:
                response = await response.json()
                return response["access_token"], response["user_id"]
            
    async def get_vk_user(self, token: str, user_id: int) -> dict:
        async with ClientSession() as session:
            async with session.get(
                f"{self.vk_config.VK_API_URL}/users.get",
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
                f"{self.yandex_config.YANDEX_API_URL}",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"OAuth {access_token}"
                },
                ssl=False
            ) as response:
                return await response.json()