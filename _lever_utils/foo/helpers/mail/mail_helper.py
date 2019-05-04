# -*- coding:utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os



class Mail(object):
    def __init__(self, server, port, username, password, sender):
        self._server = server
        self._port = port
        self._username = username
        self._password = password
        self._sender = sender

    def send(self, subject, to, cc=[], text=None, html=None, files=[]):
        try:
            # 构造邮件对象MIMEMultipart对象
            # mixed为附件邮件类型
            msg = MIMEMultipart('mixed')
            msg['Subject'] = subject
            msg['From'] = self._sender
            msg['To'] = ";".join(to)
            msg['Cc'] = ";".join(cc)
            mime_text = MIMEText(html, 'html', 'utf-8') if html is not None else MIMEText(text, 'plain', 'utf-8')
            msg.attach(mime_text)

            for file in files:
                if isinstance(file, str):
                    file = file.decode("utf-8")
                basename = os.path.basename(file)
                # 构造附件
                sendfile = open(file, 'rb').read()
                text_att = MIMEText(sendfile, 'base64', 'utf-8')
                text_att["Content-Type"] = 'application/octet-stream'
                text_att["Content-Disposition"] = 'attachment; filename=%s' % basename.encode("gb2312")
                msg.attach(text_att)

            # 发送邮件
            smtp = smtplib.SMTP_SSL(self._server, self._port)
            smtp.set_debuglevel(0)
            smtp.ehlo()
            smtp.login(self._username, self._password)
            err = smtp.sendmail(self._sender, to+cc, msg.as_string())
            smtp.close()
            if not err:
                send_result = True, None
            else:
                send_result = False, err
        except Exception, e:
            send_result = False, e
        return send_result
