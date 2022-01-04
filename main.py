import json
from zfnew import *
from config import *
from tool import *
import datetime
from datetime import timedelta

# 登陆教务平台
lgn = Login(base_url=BASE_URL)
lgn.login(STUDENT_INF['student_ID'], STUDENT_INF['password'])
cookies = lgn.cookies  # cookiejar类cookies获取方法
person = GetInfo(base_url=BASE_URL, cookies=cookies)

# 企业微信信息推送
alert = WechatAlert(corpid=CORP['id'], corpsecret=CORP['secrt'])

# 获取校历
xl_data = person.get_xiaoli()
time = datetime.datetime.strptime(xl_data['xnf'], '%Y-%m-%d')
# 获取课表
schedule_data = person.get_schedule(time.year, xl_data['xqs'])
schedule_data = json.dumps(schedule_data)

def sch2ics(kb_data):
    cal = Calendar()
    week_start = time - timedelta(days=time.weekday())
    week_str = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
    for kb in kb_data['normalCourse']:
        week = kb['Week'].replace('周', '').split(',')
        day = int(kb['Day'])
        summary = kb['Title']
        location = kb['Address']
        description = kb['Teacher']+'/'+kb['Character']+'/'+kb['Method']
        lesson = kb['Lesson'].split('-')
        stahou = datetime.datetime.strptime(
            CLASS_LIST[int(lesson[0])-1][0], '%H:%M').hour
        endhou = datetime.datetime.strptime(
            CLASS_LIST[int(lesson[1])-1][1], '%H:%M').hour
        stamin = datetime.datetime.strptime(
            CLASS_LIST[int(lesson[0])-1][0], '%H:%M').minute
        endmin = datetime.datetime.strptime(
            CLASS_LIST[int(lesson[1])-1][1], '%H:%M').minute
        for value in week:
            value = value.split('-')
            value = [int(x) for x in value]
            start_data = week_start + \
                timedelta(days=(value[0]-1)*7+day-1,
                          hours=stahou, minutes=stamin)
            end_data = week_start + \
                timedelta(days=(value[0]-1)*7+day-1,
                          hours=endhou, minutes=endmin)
            time_format = "{date.year}{date.month:0>2d}{date.day:0>2d}T{date.hour:0>2d}{date.minute:0>2d}00"
            dtstam = start_data.strftime("%Y%m%dT%H%M%SZ")
            dt_start = time_format.format(date=start_data)
            dt_end = time_format.format(date=end_data)
            if(len(value) == 1):
                count = '1'
            else:
                count = value[1]-value[0]+1
            # 如果有单双周可以在这里适配
            rrule = 'FREQ=WEEKLY;COUNT='+str(count)+';BYDAY='+week_str[day-1]
            ev = cal.new_event(summary, dtstam, dt_start, dt_end,
                               rrule, location, description)
            cal.add_event(ev)
    cal.save_as_ics_file()

    
fo = open("schedule.json", "r")
cache_data = fo.read()
if schedule_data != cache_data:
    fo.close()
    fo = open("schedule.json", "w")
    fo.write(schedule_data)
    fo.close()
    schedule_data = json.loads(schedule_data)
    sch2ics(schedule_data)
else:
    fo.close()
