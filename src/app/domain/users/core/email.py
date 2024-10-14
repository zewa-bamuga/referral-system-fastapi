import smtplib
from email.message import EmailMessage


class ReferralCodeSender:
    def __init__(self, email_address: str, email_password: str):
        self.email_address = email_address
        self.email_password = email_password

    async def send_referral_code(self, email: str, code: str):
        msg = EmailMessage()
        msg['Subject'] = "Приглашение"
        msg['From'] = self.email_address
        msg['To'] = email

        html_content = f"""\
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #003366; background-color: #486DB5;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #ffffff;">
                <h2 style="color: #FFD700;">Реферальная система</h2>
                <p>Здравствуйте,</p>
                <p>Ваш код:</p>
                <p style="font-size: 18px; font-weight: bold; color: #FFD700;">{code}</p>
                <p style="margin-top: 20px; color: #777; font-size: 12px;">Если у вас возникли какие-либо вопросы, пожалуйста, свяжитесь с нами.</p>
            </div>
        </body>
        </html>
        """

        msg.set_content(
            f"Здравствуйте,\n\nВаш код: {code}\n\n"
        )
        msg.add_alternative(html_content, subtype='html')

        await self._send_email(msg)

    async def _send_email(self, msg: EmailMessage):
        with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
            smtp.login(self.email_address, self.email_password)
            smtp.send_message(msg)
