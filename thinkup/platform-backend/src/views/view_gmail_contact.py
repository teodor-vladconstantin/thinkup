import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.jwt_server import require_auth

from flask import Blueprint, make_response, request

urlContact = Blueprint('views', __name__)

contact_mail = 'calex2005cj@gmail.com'
contact_mail2 = 'contact@think-up.academy'
# contact_mail2 = 'marc.vana@think-up.academy'
contact_password = 'vgvtmmgaafazrnfn'
contact_password2 = 'kbwkgizkkaotelyc'


MAIL_SUBJECT = "Thinkup FORM"


@urlContact.route('/contact', methods = ['POST'])
@require_auth()
def sendContactInfo():
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
