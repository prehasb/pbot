import pandas as pd
from User import User

DATABASE_PATH = "./src/database/database.csv"
STATE = "state"

STATE_TABLE_PATH = "./src/database/state_table.csv"
STATE_ID = "state_id"
ENGLISG_NAME = "english_name"
NAME = "name"

import datetime as dt

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_NAN = "2000-01-01 00:00:00"

class State(User):
    '''state抽象类'''
    
    state_id:int
    '''物品id'''
    
    def __init__(self, user_id:int, state_id:int):
        super(State, self).__init__(user_id=user_id, database_path=DATABASE_PATH)
        self.state_id = state_id
        self._update()
    
    def _update(self):
        '''更新自己的属性'''
        super()._update()
        name_in_useritem = self.getEnglishName()
        t=self.read(name_in_useritem)
        if t == None:
            self.number = 0
            self.write(name_in_useritem, 0)
        else:
            self.number = int(float(t))
    
    @classmethod
    def getNamebyId(self, state_id) -> str:
        '''查询名称'''
        item_table = pd.read_csv(STATE_TABLE_PATH, encoding="gb2312")
        name = item_table.at[state_id, NAME]
        return name
    
    @classmethod
    def getName(self) -> str:
        '''查询名称'''
        name = self.getNamebyId(self.state_id)
        return name
    
    @classmethod
    def getEnglishNamebyId(self, state_id) -> str:
        '''查询英文名称'''
        item_table = pd.read_csv(STATE_TABLE_PATH, encoding="gb2312")
        name_in_useritem = item_table.at[state_id, STATE_TABLE_PATH]
        return name_in_useritem
    
    def getEnglishName(self) -> str:
        '''查询英文名称'''
        return self.getEnglishNamebyId(self.state_id)
    
    def update(self):
        '''根据时间更新状态，删除超时状态'''
        state_info_str:str = self.read(STATE)
        # state_info: "state1:2025-04-22 00:57:40|state2:5"
        state_info_list:list = state_info_str.split("|")
        # 格式1 状态:结束时间
        _exist = False
        for state_info in state_info_list:
            state_info:str
            s = state_info.split(":")
            end_time:dt.datetime = dt.datetime.strptime(s[1], TIME_FORMAT)
            now_time = dt.datetime.now()
            if now_time > end_time:
                # delete this state
                pass
        
    
    def exist(self) -> bool:
        '''判断用户是否存在状态'''
        self.update()
        state_info_str:str = self.read(STATE)
        # state_info: "state1:2025-04-22 00:57:40|state2:5"
        state_info_list:list = state_info_str.split("|")
        # 格式1 状态:结束时间
        _exist = False
        for state_info in state_info_list:
            state_info:str
            s = state_info.split(":")
            state_name:str = s[0]
            if state_name == self.getEnglishName():
                _exist = True
                break
        
        return _exist
        
        # 格式2 状态:剩余次数
        
    
    @classmethod
    def describe(self) -> str:
        msg = ""
        msg += f"\r\n暂无该状态{self.getName()}的描述"
        return msg

    
    
    