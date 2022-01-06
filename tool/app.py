# -*- coding: utf-8 -*-

from datetime import timedelta
from datetime import datetime
import json


class App():
    """
    工具对象
    """
    def __init__(self):
        self.__config={
            'kb':'schedule.json',
            'ics': 'schedule.ics',
        }
        self.__data = {
            'kb' : self.read_file('kb')
        }

    def read_file(self, type):
        """
        读取文件数据(json)
        :param type: 类型
        :return: 数据
        """
        file_path = self.__config[type]
        with open(file_path, 'r') as f:
            return json.loads(f.read())

    def change_file(self,type, data, qiangzhi=0):
        """
        比较数据，不同则写入
        :param type: 类型
        :param data: 比较的数据
        :return: 0/1
        """
        file_path = self.__config[type]
        with open(file_path, 'w', encoding='utf8') as f:
            if(qiangzhi):
                f.write(data)
                return 1
            elif (data != self.__data[type]):
                self.__data[type] = json.loads(data)
                f.write(data)
                return 1
            else:
                return 0

    def sch2ics(self, class_list, kaxue_date):
        """
        将课表数据转换为日历数据
        :param class_list: 节次上课时间列表
        :param kaxue_date: 第一周的周一
        :return: 日历数据
        """
        kb_data = self.__data['kb']['normalCourse']
        re_data=[]
        kaxue_da = datetime.strptime(kaxue_date, '%Y-%m-%d') #开学日期
        kaxue_da = kaxue_da - timedelta(days=kaxue_da.weekday()) #开学的周一
        def less2time(lesson):
            """
            根据节次转为对应时间
            :param lessont: 节次
            :return: 上，下课的时与分
            """
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
            """
            根据周次转为对应时间
            :param week: 周次
            :return: 对应周次的周一，及循环次数
            """
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
        # 遍历课表转换数据
        week_str = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
        for kb in kb_data:
            day = [int(kb['Day'])]
            day.append(week_str[day[0]-1])
            lesson = less2time(kb['Lesson'])
            week = kb['Week'].replace('周', '').split(',')
            for value in week:  # 遍历周次
                weekdata=week2date(value)
                start_time = weekdata['start'] + timedelta(days=day[0]-1,hours=lesson['start'][0], minutes=lesson['start'][1])
                end_time = weekdata['start'] + timedelta(days=day[0]-1,hours=lesson['end'][0], minutes=lesson['end'][1])
                time_format = "{date.year}{date.month:0>2d}{date.day:0>2d}T{date.hour:0>2d}{date.minute:0>2d}00"
                data = {
                    'summary': kb['Title'],
                    'dtstamp': start_time.strftime("%Y%m%dT%H%M%SZ"),
                    'dtstart': time_format.format(date=start_time),
                    'dtend': time_format.format(date=end_time),
                    'rrule': 'FREQ=WEEKLY;COUNT='+weekdata['count']+';BYDAY='+day[1],
                    'location': kb['Address'],
                    'description': kb['Teacher']+'/'+kb['Character']+'/'+kb['Method']
                }
                re_data.append(data)
        return re_data
