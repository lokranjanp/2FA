import smtplib
from email.mime.text import MIMEText
import dotenv

# Load environment variables from .env file
path = ".env"

def send_mail(recipient_email, otp):
    """
    Sends an email to the recipient's email address with the OTP for 2FA.

    Args:
        recipient_email (str): The email address of the recipient.
        otp (str): The one-time password to be sent for 2FA.

    Returns:
        None
    """
    # Retrieve email credentials and server details from environment variables
    EMAIL_ADDRESS = dotenv.get_key(path, "EMAIL_ADDRESS")
    EMAIL_PASSWORD = dotenv.get_key(path, "EMAIL_PASSWORD")
    SMTP_SERVER = dotenv.get_key(path, "SMTP_SERVER")
    SMTP_PORT = int(dotenv.get_key(path, "SMTP_PORT"))

    # Set up the SMTP server connection
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    # Create the email message
    message = MIMEText(f"Your OTP for 2FA login @lokranjan authentication gateway is {otp}.\n"
                       f"Please do not share this OTP with anyone.\n"
                       f"Keep visiting us\n"
                       f"Regards,\nLokranjan")
    message["Subject"] = "OTP for 2FA Login"
    message["From"] = EMAIL_ADDRESS
    message["To"] = recipient_email

    # Send the email
    server.sendmail(EMAIL_ADDRESS, recipient_email, message.as_string())

    # Close the SMTP server connection
    server.quit()