import requests
import json


class WechatAlert():
    def __init__(self, corpid, corpsecret):
        self.url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        self.corpid = corpid
        self.corpsecret = corpsecret

    def get_token(self):
        # 获取token时，携带企业id和secret(注册企业号时，后台可查)
        url = self.url
        values = {'corpid': self.corpid,
                  'corpsecret': self.corpsecret,
                  }
        req = requests.get(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def send_msg(self, values):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.get_token()
        values = {
            "touser": "af",
            "msgtype": "text",
            "agentid": "1000002",
            "text": {
                      "content": values   # 要推送的内容
            }
        }
        requests.post(url, json=values)
