import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.jwt_server import require_auth
from utils.logger import setup_logger

from flask import Blueprint, make_response, request, abort

logger = setup_logger(__name__)

urlContact = Blueprint('views', __name__)

contact_mail = 'calex2005cj@gmail.com'
contact_mail2 = 'contact@think-up.academy'
# contact_mail2 = 'marc.vana@think-up.academy'
contact_password = os.environ.get('CONTACT_MAIL_PASSWORD')
contact_password2 = os.environ.get('CONTACT_MAIL_PASSWORD2')

if not contact_password:
    logger.error(
        "CONTACT_MAIL_PASSWORD is not set - the /contact endpoint will refuse "
        "to send email until it is added to .env and the backend is restarted."
    )


MAIL_SUBJECT = "Thinkup FORM"


@urlContact.route('/contact', methods = ['POST'])
@require_auth()
def sendContactInfo():
    if not contact_password:
        logger.error("Refusing to send contact email: CONTACT_MAIL_PASSWORD is missing from the environment.")
        abort(500, description="Contact form is misconfigured (missing SMTP credentials) - message was not sent")

    dataJSON = request.json

    mail = MIMEMultipart("alternative")
    mail['Subject'] = MAIL_SUBJECT
    mail['From'] = contact_mail
    mail['To'] = contact_mail2

    message = f'''FullName: {dataJSON["fullname"]}
Email: {dataJSON["email"]}
Message: {dataJSON["message"]}
'''
#   Category: {dataJSON["category"]}

    mail.attach(MIMEText(message))

    mailer = smtplib.SMTP('smtp.gmail.com',587)
    mailer.starttls()
    mailer.login(contact_mail, contact_password)
    mailer.sendmail(contact_mail, contact_mail2, mail.as_string())
    mailer.quit()

    res = make_response("ok", 200)
    return res
