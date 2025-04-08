import os
from pathlib import Path
from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from starlette.templating import Jinja2Templates

from backend.core.clients.aws_client import AWSClient
from backend.core.tasks_manager.manager import TasksManager
from backend.utils.enums import EmailServices
from backend.infrastructure.config.smtp_configs import YANDEX_SMTP_CONFIG


class SMTPClients:
    def __init__(self, tasks_manager: TasksManager):
        self.yandex_smtp = FastMail(self.create_yandex_config())
        self.tasks_manager = tasks_manager
        # self.google_smtp = FastMail(self.create_google_config())
        self.templates = Jinja2Templates(directory=self._get_path_to_templates())

    def _get_path_to_templates(self):
        return Path(__file__).resolve().parent.parent.parent / "utils" / "email_templates"
    def create_yandex_config(self):
        return ConnectionConfig(
            MAIL_USERNAME=YANDEX_SMTP_CONFIG.YANDEX_SMTP_USER,
            MAIL_PASSWORD=YANDEX_SMTP_CONFIG.YANDEX_SMTP_PASSWORD,
            MAIL_PORT=YANDEX_SMTP_CONFIG.YANDEX_SMTP_PORT,
            MAIL_SERVER=YANDEX_SMTP_CONFIG.YANDEX_SMTP_HOST,
            MAIL_STARTTLS=True, 
            MAIL_SSL_TLS=False, 
            MAIL_FROM=YANDEX_SMTP_CONFIG.YANDEX_SMTP_USER,
            VALIDATE_CERTS=False
        )

    # def create_google_config(self):
    #     google_config = load_google_smtp_config()
    #     return ConnectionConfig(
    #         MAIL_USERNAME=google_config.GOOGLE_SMTP_USER,
    #         MAIL_PASSWORD=google_config.GOOGLE_SMTP_PASSWORD,
    #         MAIL_PORT=google_config.GOOGLE_SMTP_PORT,
    #         MAIL_SERVER=google_config.GOOGLE_SMTP_HOST,
    #         MAIL_STARTTLS=True,
    #         MAIL_SSL_TLS=False,
    #         MAIL_FROM=google_config.GOOGLE_SMTP_USER
    #     )

    async def _send_email(self, message: MessageSchema, service: str, email: str):
        if service == EmailServices.YANDEX.value:
            await self.tasks_manager.add_base_task(
                self.yandex_smtp.send_message, 
                namespace=f"verify_email_{email}",
                task_name="send_email",
                func_args=(message,)
            )
        elif service == EmailServices.GOOGLE.value: 
            self.tasks_manager.add_task(self.google_smtp.send_message, message)

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
        service = email.split("@")[1].split(".")[0]
        await self._send_email(message, service, email)
    
    async def invite_members(self, emails: list[str]):
        template = self.templates.get_template("invite_member.html")
        message = MessageSchema(
            subject="Invite members",
            recipients=emails,
            body=template.render(),
            subtype="html"
        )

        for email in emails:
            service = email.split("@")[1].split(".")[0]
            await self._send_email(message, service, email)
