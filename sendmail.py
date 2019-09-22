#!/usr/bin/env python3
# coding=utf-8
import imghdr
import mimetypes
import os
import smtplib
from email.headerregistry import Address
from email.message import EmailMessage


class Mail:
    def __init__(self, smtp_server='', smtp_port='', username='', display_name='',
                 password='', receivers=None, cc=None, subject='', content='',
                 files=None, images=None):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.display_name = display_name
        self.subject = subject
        self.content = content
        if files is None:
            files = []
        self.files = files
        if images is None:
            images = []
        self.images = images
        if cc is None:
            cc = []
        self.cc = cc
        if receivers is None:
            receivers = []
        self.receivers = receivers
        return

    def send(self):
        smtp = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        smtp.ehlo_or_helo_if_needed()
        smtp.login(self.username, self.password)

        msg = EmailMessage()
        msg['subject'] = self.subject
        msg['from'] = Address(self.display_name, addr_spec=self.username)
        msg['to'] = ', '.join(self.receivers)
        if self.cc:
            msg['cc'] = ','.join(self.cc)
        msg.add_alternative(self.content, subtype='html')
        for file in self.files:
            if not os.path.isfile(file):
                continue
            ctype, encoding = mimetypes.guess_type(file)
            if ctype is None or encoding is not None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            with open(file, 'rb') as fp:
                msg.add_attachment(fp.read(),
                                   maintype=maintype,
                                   subtype=subtype,
                                   filename=file)
        for image in self.images:
            if not os.path.isfile(image):
                print('not found:', image)
                continue
            with open(image, 'rb') as fp:
                image_type = imghdr.what(image)
                msg.add_attachment(fp.read(), 'image', image_type, cid=image)
        smtp.send_message(msg)
        smtp.quit()
        return


if __name__ == '__main__':
    m = Mail()
    m.username = 'xxxxxxxx@qq.com'
    m.display_name = 'xxxx'
    m.password = 'xxxxxxxx'
    m.receivers = ['xxxxxxxx@xxx.com']
    m.smtp_server = 'smtp.qq.com'
    m.smtp_port = 465
    m.subject = 'test'
    m.files = ['test.zip']
    # m.images = ['p2561529786.jpg', 'p2561529786.jpg']
    # m.content = 'hello<img src="cid:p2561529786.jpg"/>\n<img src="cid:p2561529786.jpg"/>'
    m.content = 'hello, this is a test mail.'
    m.send()
