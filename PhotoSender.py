from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

from Variables import PASSWORD

app = Flask(__name__)

def send_test_mail(body):
    sender_email = "navacartest@mail.ru"
    receiver_email = "navacar@mail.ru"

    msg = MIMEMultipart()
    msg['Subject'] = '[Email Test]'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with open('Resources/example.jpg', 'rb') as fp:
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename="example.jpg")
        msg.attach(img)

    try:
        with smtplib.SMTP('smtp.mail.ru', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login("navacartest@mail.ru", PASSWORD)
            smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    send_test_mail("Welcome to Medium!")
    app.run('0.0.0.0',port=5000)