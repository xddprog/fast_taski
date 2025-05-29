from multiprocessing import Process
from pathlib import Path
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from starlette.templating import Jinja2Templates

from backend.infrastructure.config.smtp_configs import YANDEX_SMTP_CONFIG
from backend.core.tasks_manager.manager import TasksManager


class SMTPClients:
    def __init__(self, tasks_manager: TasksManager = None):
        self.tasks_manager = tasks_manager
        self.yandex_smtp = FastMail(self.create_yandex_config())
        self.templates = Jinja2Templates(directory=self._get_path_to_templates())

    def _get_path_to_templates(self):
        return Path(__file__).resolve().parent.parent.parent / "utils" / "templates"
    
    def create_yandex_config(self):
        return ConnectionConfig(
            MAIL_USERNAME=YANDEX_SMTP_CONFIG.YANDEX_SMTP_USER,
            MAIL_PASSWORD=YANDEX_SMTP_CONFIG.YANDEX_SMTP_PASSWORD,
            MAIL_PORT=YANDEX_SMTP_CONFIG.YANDEX_SMTP_PORT,
            MAIL_SERVER=YANDEX_SMTP_CONFIG.YANDEX_SMTP_HOST,
            MAIL_STARTTLS=False, 
            MAIL_SSL_TLS=True, 
            MAIL_FROM=YANDEX_SMTP_CONFIG.YANDEX_SMTP_USER,
            SUPPRESS_SEND=0,
            TIMEOUT=10
        )

    async def send_verification_code(
        self, 
        email: str, 
        code: str, 
        username: str,
    ) -> None:
        template = self.templates.get_template("verification_code.html")
        message = MessageSchema(
            subject="Verification code",
            recipients=[email],
            body=template.render(name=username, otp=code),
            subtype="html"
        )
        await self.yandex_smtp.send_message(message)
    
    async def invite_members(self, emails: list[str], team_id, team_name: str, token: str):
        template = self.templates.get_template("invite_member.html")
        message = MessageSchema(
            subject="Invite members",
            recipients=emails,
            body=template.render(team_name=team_name, token=token, team_id=team_id),
            subtype="html"
        )
        await self.yandex_smtp.send_message(message)