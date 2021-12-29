import json
from zfnew import *
from config import *
from tool import *

# 登陆
lgn = Login(base_url=BASE_URL)
lgn.login(STUDENT_INF['student_ID'], STUDENT_INF['password'])
cookies = lgn.cookies  # cookiejar类cookies获取方法
person = GetInfo(base_url=BASE_URL, cookies=cookies)

alert = WechatAlert(corpid=CORP['id'], corpsecret=CORP['secrt'])


# 缓存课表
data = json.dumps(person.get_grade('2021', '1'))
fo = open("cache.json", "r")
cache_data = fo.read()
if data != cache_data:
    fo.close()
    fo = open("cache.json", "w")
    fo.write(data)
    fo.close()
    alert.send_msg("新成绩！")
else:
    fo.close()
