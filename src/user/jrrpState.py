from User import User
import datetime as dt
from datetime import datetime
import pandas as pd
import numpy as np  # 用于生成 NaN 值

JRRP = "jrrp_value"
JRRPTIME = "jrrp_next_time"

TIME_NAN = "2000-01-01 00:00:00"
TEXT = "text"

THRESHOLD_HOUR = 22
'''jrrp更新时间为22:00'''
THRESHOLD_MINUTE = 0
'''jrrp更新时间为22:00'''

JRRP_TEXT_PATH = "./src/database/jrrp_text.csv"

class jrrpState(User):

    value : int = None
    '''jrrp值'''
    next_time : datetime = None
    '''jrrp时间'''
    
    def __init__(self, user_id : int):
        super(jrrpState, self).__init__(user_id=user_id)
        self._update()
    
    def __str__(self) -> str:
        return super().__str__() + f"今日人品:{self.value}\r\n今日人品时间{self.next_time}\r\n"
    
    def _update(self):
        '''更新自己的状态'''
        super()._update() # 更新父类
        
        # 更新jrrp_value(进行空检测)
        if str(self.read(JRRP)) == "nan":
            self.value = -1
        else:
            self.value = int(self.read(JRRP))
        
        # 更新next_time(进行空检测)
        date_format = "%Y-%m-%d %H:%M:%S"
        if str(self.read(JRRPTIME)) == "nan":
            self.next_time = datetime.strptime(TIME_NAN, date_format)
        else:
            self.next_time = datetime.strptime(self.read(JRRPTIME), date_format)
        
        
    def set_next_time(self):
        '''设置下次jrrp的时间阈值'''
        # 1、获取当前时间
        current_time = dt.datetime.now()
        current_date = current_time.date()
        current_hour = current_time.time().hour
        current_minute = current_time.time().minute
        
        # 2、还没到时间，返回值为当天10点
        if current_hour < THRESHOLD_HOUR or (current_hour == THRESHOLD_HOUR and current_minute < THRESHOLD_MINUTE):
            next_date = current_date
        # 2.1、过了时间，返回值为下一天10点
        else:
            next_date = current_date + dt.timedelta(days=1)
            
        # 3、整理时间，输出返回值
        self.next_time = dt.datetime.combine(next_date, dt.time(THRESHOLD_HOUR, THRESHOLD_MINUTE))
        self.write(JRRPTIME,self.next_time)
        
    def set_jrrp(self, jrrp_value : int):
        '''保存用户当天的jrrp值'''
        self.write(JRRP, str(jrrp_value))
        self._update()
    
    def jrrped(self) -> bool:
        '''检测用户当天是否进行过jrrp'''
        current_time = dt.datetime.now()
        if self.next_time == np.nan:
            return False
        return (current_time < self.next_time)
    
    def get_jrrp_text(self) -> str:
        jrrp_text_table = pd.read_csv(JRRP_TEXT_PATH, encoding="gb2312")
        # jrrp_text_table: (example)
        #      jrrp      text
        # 0     0         t0
        # 1     1         t1
        # ...
        # 77    77        t77
        # ...
        # 100  100       t100
        
        # self.value = 77
        text = jrrp_text_table.at[self.value, TEXT] # text = jrrp_text_table.at[77, "text"] 
        
        return text # return "t77"
    