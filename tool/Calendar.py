# -*- coding: utf-8 -*-

class Calendar:
    """
    日历对象
    """

    def __init__(self, calendar_name="schedule"):
        self.__events = {}
        self.__event_id = 0
        self.calendar_name = calendar_name
    
    def new_event(self, SUMMARY, DTSTAMP, DTSTART, DTEND, RRULE, LOCATION, DESCRIPTION):
        """
        新建一个事件
        :param SUMMARY: 事件名
        :param DTSTAMP: 开始时间
        :param DTSTART: 开始时间
        :param DTEND: 结束时间
        :param RRULE: 循环设置
        :param LOCATION: 地点
        :param DESCRIPTION: 备注
        :return:
        """
        event_text=''
        event_data = {
            'BEGIN': 'VEVENT',
            'CLASS': 'PUBLIC',
            'CREATED': DTSTAMP,
            'SUMMARY': SUMMARY,
            'DTSTAMP': DTSTAMP,
            'DTSTART;TZID=Asia/Shanghai': DTSTART,
            'DTEND;TZID=Asia/Shanghai': DTEND,
            'LAST_MODIFIED': DTSTAMP,
            'RRULE':RRULE,
            'LOCATION': LOCATION,
            'DESCRIPTION': DESCRIPTION,
            'END': 'VEVENT'
        }
        for item, data in event_data.items():
            event_text += "%s:%s\n" % (item, data)
        return event_text
    
    def add_event(self,da_str):
        """将事件添加到日历"""
        self.__events[self.__event_id] = da_str
        self.__event_id += 1
        # return event_id

    def get_ics_text(self):
        """获取日历ics数据"""
        self.__calendar_text = """BEGIN:VCALENDAR\nPRODID:-//ZHONG_BAI_REN//APPGENIX-SOFTWARE//\nVERSION:2.0\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:%s\nX-WR-TIMEZONE:null\n""" % self.calendar_name
        for value in self.__events.values():
            self.__calendar_text += value
        self.__calendar_text += "END:VCALENDAR"
        return self.__calendar_text

    # def save_as_ics_file(self):
    #     ics_text = self.get_ics_text()
    #     open("%s.ics" % self.calendar_name, "w", encoding="utf8").write(
    #         ics_text)  # 使用utf8编码生成ics文件，否则日历软件打开是乱码
