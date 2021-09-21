###############################################################################
# Copyright (c), 2021 nK ind.                                                 #
#                                                                             #
#                                                                             #
# PhotoSender.py - recive email with code and send on it corresponding photo  #
#                                                                             #
#                                                                             #
# @created 2021-09-21 by Alexandr Navasardyan                                 #
###############################################################################

import smtplib
import imaplib

import email

from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from Variables import PASSWORD

emailAdress = "navacartest@mail.ru"
server = "smtp.mail.ru"
imapServer = "imap.mail.ru"
port = 587

def deleteMessage(reciver):
    imap = imaplib.IMAP4_SSL(imapServer)
    imap.login(emailAdress, PASSWORD)
    imap.select('inbox')
    status, messages = imap.search(None, f'FROM {reciver}')
    messages = messages[0].split(b' ')

    for mail in messages:
        msg = imap.fetch(mail, "(RFC822)")
    
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject = decode_header(msg["Subject"])[0][0]
                
                if isinstance(subject, bytes):
                    subject = subject.decode()
                
                print("Deleting", subject)
        imap.store(mail, "+FLAGS", "\\Deleted")
    
    imap.expunge()
    imap.close()
    imap.logout()


def receiveEmail():
    mail = imaplib.IMAP4_SSL(imapServer)
    mail.login(emailAdress, PASSWORD)
    mail.select('inbox')
    
    status, data = mail.search(None, 'ALL')
    
    mail_ids = []
    for block in data:
        mail_ids += block.split()

    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')
    
        for response_part in data:
            
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])

                mail_from = message['from']
                mail_subject = message['subject']

                if message.is_multipart():
                    mail_content = ''
                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()

    return mail_from, mail_content

def send_test_mail(reciver, imageCode):
    msg = MIMEMultipart()
    msg['Subject'] = '[Email Test]'
    msg['From'] = emailAdress
    msg['To'] = reciver

    image = "Resources/" + str(imageCode) + ".jpg"

    with open(image, 'rb') as fp:
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename="example.jpg")
        msg.attach(img)

    try:
        with smtplib.SMTP(server, port) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(emailAdress, PASSWORD)
            smtpObj.sendmail(emailAdress, reciver, msg.as_string())
            smtpObj.quit()
    except Exception as e:
        print(e)    

reciver, code = receiveEmail()
send_test_mail(reciver, int(code))
# deleteMessage(reciver)
