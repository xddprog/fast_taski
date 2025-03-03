from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from starlette.templating import Jinja2Templates

from backend.core.config.smtp_configs import load_google_smtp_config, load_yandex_smtp_config
from backend.core.enums import EmailServices


class SMTPClients:
    def __init__(self):
        self.yandex_smtp = FastMail(self.create_yandex_config())
        # self.google_smtp = FastMail(self.create_google_config())
        self.templates = Jinja2Templates(directory="/Users/mago/Documents/fastapi-auth/backend/utils/email_templates")

    def create_yandex_config(self):
        yandex_config = load_yandex_smtp_config()
        return ConnectionConfig(
            MAIL_USERNAME=yandex_config.YANDEX_SMTP_USER,
            MAIL_PASSWORD=yandex_config.YANDEX_SMTP_PASSWORD,
            MAIL_PORT=yandex_config.YANDEX_SMTP_PORT,
            MAIL_SERVER=yandex_config.YANDEX_SMTP_HOST,
            MAIL_STARTTLS=True, 
            MAIL_SSL_TLS=False, 
            MAIL_FROM=yandex_config.YANDEX_SMTP_USER,
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

    async def send_verification_code(
        self, 
        email: str, 
        code: str, 
        username: str,
        background_tasks: BackgroundTasks
    ) -> None:
        template = self.templates.get_template("verification_code.html")
        message = MessageSchema(
            subject="Verification code",
            recipients=[email],
            body=template.render(name=username, otp=code),
            subtype="html"
        )
        service = email.split("@")[1].split(".")[0]

        if service == EmailServices.YANDEX.value:
            background_tasks.add_task(self.yandex_smtp.send_message, message)
        elif service == EmailServices.GOOGLE.value: 
            background_tasks.add_task(self.google_smtp.send_message, message)
        return 