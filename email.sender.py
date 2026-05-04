import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import *
from logger import log_info, log_error

def load_template(user):
    with open("template.html", "r") as file:
        html = file.read()

    html = html.replace("{{name}}", user["name"])
    html = html.replace("{{role}}", user["role"])
    html = html.replace("{{domain}}", user["domain"])

    return html

def send_email(user):
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        msg = MIMEMultipart("alternative")
        msg["From"] = SENDER_EMAIL
        msg["To"] = user["email"]
        msg["Subject"] = f"Opportunity for {user['role']} in {user['domain']}"

        html_content = load_template(user)
        msg.attach(MIMEText(html_content, "html"))

        server.send_message(msg)
        server.quit()

        log_info(f"Email sent to {user['email']}")
        return "Sent", None

    except Exception as e:
        log_error(f"Failed to send email to {user['email']} - {str(e)}")
        return "Failed", str(e)