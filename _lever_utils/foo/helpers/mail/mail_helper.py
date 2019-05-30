# -*- coding:utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from datetime import datetime



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


class MailServer(object):
    SF = "%Y-%m-%d %H:%M:%S"
    pop3_server = None
    args_pop_server = None
    args_user = None
    args_password = None

    def __init__(self, pop_server, user, password):
        self.args_pop_server = pop_server
        self.args_user = user
        self.args_password = password
        self._restart()

    def quit(self):
        if self.pop3_server is not None:
            self.pop3_server.quit()
            self.pop3_server = None

    def _restart(self):
        self.quit()
        tmp_pop3_server = poplib.POP3(self.args_pop_server)
        tmp_pop3_server.user(self.args_user)
        tmp_pop3_server.pass_(self.args_password)
        self.pop3_server = tmp_pop3_server

    def get(self, *args):
        self._restart()
        res = {}
        for arg in args:
            if arg == 'stat':
                res[arg] = self.pop3_server.stat()[0]
            elif arg == 'list':
                res[arg] = self.pop3_server.list()
            elif arg == 'latest':
                mails = self.pop3_server.list()[1]
                resp, lines, octets = self.pop3_server.retr(len(mails))
                msg = Parser().parsestr(b'\r\n'.join(lines))
                res[arg] = self._parse_message(msg)
            elif type(arg) == int:
                mails = self.pop3_server.list()[1]
                if arg > len(mails):
                    res[arg] = None
                    continue
                resp, lines, octets = self.pop3_server.retr(arg)
                msg = Parser().parsestr(b'\r\n'.join(lines))
                res[arg] = self._parse_message(msg)
            else:
                res[arg] = None
        return res

    def _parse_message(self, msg):
        result = {}
        # Subject
        subject_tmp = msg.get('Subject', '')
        value, charset = decode_header(subject_tmp)[0]
        if charset:
            value = value.decode(charset)
        result['Subject'] = value
        # 'From', 'To', 'Cc'
        for header in ['From', 'To', 'Cc']:
            result[header] = []
            temp = msg.get(header, '')
            temp_list = temp.split(',')
            for i in temp_list:
                if i == '':
                    continue
                name, addr = parseaddr(i)
                value, charset = decode_header(name)[0]
                if charset:
                    value = value.decode(charset)
                tmp_addr_info = dict(name=value, addr=addr)
                result[header].append(tmp_addr_info)
        try:
            result['Date'] = datetime.strptime(msg.get('Date', ''), "%a, %d %b %Y %H:%M:%S +0800").strftime(self.SF)
        except Exception,e:
            result['Date'] = str(msg.get('Date', ''))
        result['Files'] = []
        result['Bodys'] = []
        for par in msg.walk():
            name = par.get_filename()
            if name:
                data = par.get_payload(decode=True)
                result['Files'].append(dict(name=name, data=data))
            else:
                body = par.get_payload(decode=True)
                if body is not None:
                    result['Bodys'].append(dict(body=body))

        return result
