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
import time
import email
import os

from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from Variables import PASSWORD

emailAdress = "navacartest@mail.ru"
server = "smtp.mail.ru"
imapServer = "imap.mail.ru"
smtpPort = 587
imapPort = 993

def deleteMessage():
    typ, data = mail.search(None, 'SEEN')
    for num in data[0].split():
        mail.store(num, '+FLAGS', '\\Deleted')
    mail.expunge()
    mail.close()
    mail.logout()


def receiveEmail():
    status, data = mail.search(None, 'ALL')

    mailFrom = []
    mailContent = []
    
    mailIds = []
    for block in data:
        mailIds += block.split()

    for i in mailIds:
        status, data = mail.fetch(i, '(RFC822)')
    
        for responsePart in data:
            
            if isinstance(responsePart, tuple):
                message = email.message_from_bytes(responsePart[1])

                mailFrom.append(message['from'])

                if message.is_multipart():
                    mailContentContainer = ''
                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            mailContentContainer += part.get_payload()
                else:
                    mailContentContainer = message.get_payload()
                
                mailContent.append(mailContentContainer)

    return mailFrom, mailContent

def sendTestMail(reciver, imageCode):
    msg = MIMEMultipart()
    msg['Subject'] = '[Email Test]'
    msg['From'] = emailAdress
    msg['To'] = reciver

    image = "Resources/" + str(imageCode) + ".jpg"

    if os.path.isfile(image):
        with open(image, 'rb') as fp:
            img = MIMEImage(fp.read())
            img.add_header('Content-Disposition', 'attachment', filename="example.jpg")
            msg.attach(img)

        try:
            with smtplib.SMTP(server, smtpPort) as smtpObj:
                smtpObj.ehlo()
                smtpObj.starttls()
                smtpObj.login(emailAdress, PASSWORD)
                smtpObj.sendmail(emailAdress, reciver, msg.as_string())
                smtpObj.quit()
        except Exception as e:
            print(e)
    else:
        print("Image not exist")

def representsInt(number):
    try: 
        int(number)
        return True
    except ValueError:
        return False

timing = time.time()
while True:
    if time.time() - timing > 30:

        mail = imaplib.IMAP4_SSL(imapServer)
        mail.login(emailAdress, PASSWORD)
        mail.select('inbox')

        timing = time.time()
        reciver, code = receiveEmail()
        
        if reciver and code:
            for i in range(len(reciver)):
                if representsInt(code[i]):
                    sendTestMail(reciver[i], int(code[i]))
                else:
                    print("Code is not numeric")
        else:
            print("Lists are empty")
        
        deleteMessage()
