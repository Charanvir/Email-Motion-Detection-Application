import smtplib
import ssl
# Meta data about images
import imghdr
# Build complex email objects
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()
SENDER = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER = os.getenv("EMAIL")


def send_email(image_path):
    print("Email starting")
    email_message = EmailMessage()
    email_message["Subject"] = "Motion Detected"
    email_message.set_content("Hey, we detected a motion, and have attached an image of the object in motion")

    with open(image_path, "rb") as file:
        attachment = file.read()

    email_message.add_attachment(attachment, maintype="image", subtype=imghdr.what(None, attachment))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()
    print("email ending")


if __name__ == "__main__":
    send_email("images/1.png")
