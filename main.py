import json
from zfnew import *
from config import *
from tool import *

# 登陆教务平台
lgn = Login(base_url=BASE_URL)
lgn.login(STUDENT_INF['student_ID'], STUDENT_INF['password'])
cookies = lgn.cookies  # cookiejar类cookies获取方法
person = GetInfo(base_url=BASE_URL, cookies=cookies)
# 企业微信信息推送
alert = WechatAlert(corpid=CORP['id'], corpsecret=CORP['secrt'])
# 工具封装
app = App()
cal = Calendar()

# 获取校历
xl_data = person.get_xiaoli()

# 获取课表
schedule_data = person.get_schedule(xl_data['xn_sta'], xl_data['xq_num'])
schedule_data = json.dumps(schedule_data)
# 比较缓存数据
if (app.change_file('kb', schedule_data)):
    ics_data = app.sch2ics(CLASS_LIST, xl_data['date_sta'])
    for key in ics_data:
        ev = cal.new_event(key['summary'], key['dtstamp'], key['dtstart'], key['dtend'],
                        key['rrule'], key['location'], key['description'])
        cal.add_event(ev)
    cal_data = cal.get_ics_text()
    app.change_file('ics', cal_data, 1)  # 强制存储ics
