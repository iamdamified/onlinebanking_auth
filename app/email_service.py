import smtplib
from email.message import EmailMessage
from email.utils import formataddr
import os

# Load environment variables
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# ✅ Fail fast if anything is missing
if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD]):
    raise RuntimeError(
        "SMTP environment variables are not fully set. "
        "Check SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD"
    )

# ✅ Safe conversion after validation
SMTP_PORT = int(SMTP_PORT)

SENDER_NAME = "DipHolding Bank Security Support"  # You can customize this

def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = formataddr((SENDER_NAME, SMTP_USER))
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    # ✅ Correct SMTP connection flow
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()                 # 1️⃣ Identify
        server.starttls()             # 2️⃣ Secure connection
        server.ehlo()                 # 3️⃣ Re-identify
        server.login(SMTP_USER, SMTP_PASSWORD)  # 4️⃣ Authenticate
        server.send_message(msg)      # 5️⃣ Send email