import json,config
from zfnew import *

base_url = config.BASE_URL
su_inf={
    'id': config.STUDENT_INF['student ID'],
    'pwd': config.STUDENT_INF['password']
}

# 登陆
lgn = Login(base_url=base_url)
lgn.login(su_inf['id'], su_inf['pwd'])
cookies = lgn.cookies  # cookiejar类cookies获取方法
person = GetInfo(base_url=base_url, cookies=cookies)


# 缓存课表
schedule = person.get_schedule('2021', '2')
fo = open("cache.json", "w")
fo.write(json.dumps(schedule))
fo.close()

