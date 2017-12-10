import sys
import glob
import smtplib
from config import *
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64

def send_email(ebook):
    SUBJECT = "Email Ebooks"

    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(ebook, "rb").read())
    encode_base64(part)

    part.add_header('Content-Disposition', "attachment; filename=%s" % ebook)
    msg.attach(part)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)

    try:
        server.sendmail(msg['From'], msg['To'], msg.as_string())
    except Exception as ex:
        sys.exit("Mail failed: %s" % str(ex))
    finally:
        server.close()

if len(sys.argv) > 1:
    ebook = sys.argv[1]
    send_email(ebook)
else:
    for ebook in glob.glob("ebooks/*.pdf"):
        decision = input("Do you want to send: %s? (y/n)\n" % ebook)
        if decision == 'y':
            send_email(ebook)
