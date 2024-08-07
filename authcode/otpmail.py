import smtplib
from email.mime.text import MIMEText
import dotenv
path = "../.env"

def send_mail(recipient_email, otp):
    """Sends an email to recipient's email with the OTP for 2FA"""
    EMAIL_ADDRESS = dotenv.get_key(path, "EMAIL_ADDRESS")
    EMAIL_PASSWORD = dotenv.get_key(path, "EMAIL_PASSWORD")
    SMTP_SERVER = dotenv.get_key(path, "SMTP_SERVER")
    SMTP_PORT = int(dotenv.get_key(path, "SMTP_PORT"))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    message = MIMEText(f"Your OTP for 2FA login @lokranjan authentication gateway is {otp}.\n"
                       f"Please do not share this OTP with anyone.\n"
                       f"Keep visiting us\n"
                       f"Regards,\nLokranjan")
    message["Subject"] = "OTP for 2FA Login"
    message["From"] = EMAIL_ADDRESS
    message["To"] = recipient_email
    server.sendmail(EMAIL_ADDRESS, "lokranjan03@gmail.com", message.as_string())

    server.quit()

send_mail()
