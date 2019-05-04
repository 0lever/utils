# -*- coding:utf-8 -*-
import requests
import json


class DingDing(object):
    def __init__(self, access_token):
        self._url = "https://oapi.dingtalk.com/robot/send"
        self._access_token = access_token

    def _do(self, payload):
        querystring = {"access_token": self._access_token}
        headers = {'Content-Type': "application/json"}
        response = requests.request("POST", self._url, data=json.dumps(payload), headers=headers, params=querystring)
        return response.text

    def send_text(self, content, at=[]):
        payload = \
            {
                'msgtype': 'text',
                'text': {
                    'content': content
                },
                'at': {
                    'atMobiles': at,
                    'isAtAll': False
                }
            }
        return self._do(payload=payload)

    def send_link(self, title, text, messageUrl, picUrl=""):
        payload = \
            {
                "msgtype": "link",
                "link": {
                    "text": text,
                    "title": title,
                    "picUrl": picUrl,
                    "messageUrl": messageUrl
                }
            }
        return self._do(payload=payload)

    def send_markdown(self, title, text, at=[], messageUrl="", picUrl=""):
        payload = \
            {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": "### {title}  \n> @{at}\n\n> {text}\n > ![]({picUrl})\n  > ###### [详情]({messageUrl}) ".format(
                        title=title,
                        text=text,
                        at=",".join(at),
                        picUrl=picUrl,
                        messageUrl=messageUrl
                    )
                },
                "at": {
                    "atMobiles": at,
                    "isAtAll": False
                }
            }

        return self._do(payload=payload)

    def send_actioncard(self, title, text, messageUrl="", picUrl=""):
        payload = \
            {
                "actionCard": {
                    "title": title,
                    "text": "![]({picUrl}) \n #### {title} \n\n {text}".format(picUrl=picUrl, title=title, text=text),
                    "hideAvatar": "0",
                    "btnOrientation": "0",
                    "singleTitle": "阅读详情",
                    "singleURL": messageUrl
                },
                "msgtype": "actionCard"
            }
        return self._do(payload=payload)

    def send_different_actitioncard(self, title, text, title_url_tuple_list=[], picUrl=""):
        title_url_dict_list = [{"title": i[0], "actionURL": i[1]} for i in title_url_tuple_list]
        payload = \
            {
                "actionCard": {
                    "title": title,
                    "text": "![]({picUrl}) \n\n #### {title} \n\n {text}".format(picUrl=picUrl, title=title, text=text),
                    "hideAvatar": "0",
                    "btnOrientation": "0",
                    "btns": title_url_dict_list
                },
                "msgtype": "actionCard"
            }
        return self._do(payload=payload)

    def send_feedcard(self, title_msg_pic_tuple_list):
        title_msg_pic_dict_list = [{"title": i[0], "messageURL": i[1], "picURL": i[2]} for i in title_msg_pic_tuple_list]
        payload = \
            {
                "feedCard": {
                    "links": title_msg_pic_dict_list
                },
                "msgtype": "feedCard"
            }
        return self._do(payload=payload)