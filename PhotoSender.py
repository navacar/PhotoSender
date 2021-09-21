import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from Variables import PASSWORD

def send_test_mail(reciver, imageCode):
    sender_email = "navacartest@mail.ru"
    receiver_email = reciver

    msg = MIMEMultipart()
    msg['Subject'] = '[Email Test]'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    image = "Resources/" + str(imageCode) + ".jpg"

    with open(image, 'rb') as fp:
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename="example.jpg")
        msg.attach(img)

    try:
        with smtplib.SMTP('smtp.mail.ru', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login("navacartest@mail.ru", PASSWORD)
            smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
            smtpObj.quit()
    except Exception as e:
        print(e)

send_test_mail("navacar@mail.ru", 123)