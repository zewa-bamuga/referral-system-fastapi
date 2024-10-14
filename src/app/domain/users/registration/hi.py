import smtplib
from email.message import EmailMessage

from app.domain.common.models import User


async def send_hello(user: User):
    email_address = "tikhonov.igor2028@yandex.ru"
    email_password = "abqiulywjvibrefg"

    msg = EmailMessage()
    msg['Subject'] = "Подтверждение регистрации"
    msg['From'] = email_address
    msg['To'] = user.email

    html_content = f"""\
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #003366; background-color: #486DB5;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #ffffff;">
            <h2 style="color: #FFD700;">Подтверждение регистрации</h2>
            <p>Мы рады приветствовать тебя!</p>
            <p style="margin-top: 20px; color: #777; font-size: 12px;">Если у вас возникли какие-либо вопросы, пожалуйста, свяжитесь с нами.</p>
        </div>
    </body>
    </html>
    """

    msg.set_content(
        "Мы рады приветствовать тебя!")
    msg.add_alternative(html_content, subtype='html')

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

