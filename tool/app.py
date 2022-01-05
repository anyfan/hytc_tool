from datetime import timedelta
from datetime import datetime
import json



class App:

    def __init__(self):
        self.__config={
            'kb':'schedule.json',
            'ics': 'schedule.ics',
        }
        self.__data = {
            'kb' : self.read_file('kb')
        }

    def read_file(self, type):
        file_path = self.__config[type]
        with open(file_path, 'r') as f:
            return json.loads(f.read())

    def change_file(self,type, data, qiangzhi=0):
        file_path = self.__config[type]
        with open(file_path, 'w', encoding='utf8') as f:
            if(qiangzhi):
                f.write(data)
                return 1
            elif (data != self.__data[type]):
                self.__data['kb'] = json.loads(data)
                f.write(data)
                return 1
            else:
                return 0

    def sch2ics(self, class_list, kaxue_date):
        kb_data = self.__data['kb']['normalCourse']
        re_data=[]
        kaxue_da = datetime.strptime(kaxue_date, '%Y-%m-%d')
        kaxue_da = kaxue_da - timedelta(days=kaxue_da.weekday())#第一周的星期一
        def less2time(lesson):
            less_list= lesson.split('-')
            less_list = [int(x) for x in less_list]
            start_time=class_list[less_list[0]-1][0].split(':')
            end_time = class_list[less_list[1]-1][1].split(':')
            data={
                'start': [int(start_time[0]), int(start_time[1])],
                'end': [int(end_time[0]), int(end_time[1])]
            }
            return data
        def week2date(week):
            list = week.split('-')
            list = [int(x) for x in list]
            date = kaxue_da + timedelta(days=(list[0]-1)*7)
            if(len(list) == 1):
                count = 1
            else:
                count = list[1]-list[0]+1
            data = {
                'start': date,
                'count': str(count)
            }
            return data
        week_str = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
        for kb in kb_data:
            day = [int(kb['Day'])]
            day.append(week_str[day[0]-1])
            lesson = less2time(kb['Lesson'])
            week = kb['Week'].replace('周', '').split(',')
            for value in week:
                weekdata=week2date(value)
                start_time = weekdata['start'] + timedelta(days=day[0]-1,hours=lesson['start'][0], minutes=lesson['start'][1])
                end_time = weekdata['start'] + timedelta(days=day[0]-1,hours=lesson['end'][0], minutes=lesson['end'][1])
                time_format = "{date.year}{date.month:0>2d}{date.day:0>2d}T{date.hour:0>2d}{date.minute:0>2d}00"
                dtstamp = start_time.strftime("%Y%m%dT%H%M%SZ")
                dtstart = time_format.format(date=start_time)
                dtend = time_format.format(date=end_time)
                data = {
                    'summary': kb['Title'],
                    'dtstamp': dtstamp,
                    'dtstart': dtstart,
                    'dtend': dtend,
                    'rrule': 'FREQ=WEEKLY;COUNT='+weekdata['count']+';BYDAY='+day[1],
                    'location': kb['Address'],
                    'description': kb['Teacher']+'/'+kb['Character']+'/'+kb['Method']
                }
                re_data.append(data)
        return re_data
