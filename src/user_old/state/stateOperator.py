import pandas as pd
from User import User

DATABASE_PATH = "./src/database/database.csv"
STATE = "state"

STATE_TABLE_PATH = "./src/database/state_table.csv"
STATE_ID = "state_id"
ENGLISG_NAME = "english_name"
NAME = "name"
DESCRIPTION = "description"

import datetime as dt
from datetime import datetime

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_NAN = "2000-01-01 00:00:00"

class stateOperator(User):
    '''stateOp抽象类'''
    
    def __init__(self, user_id:int):
        super(stateOperator, self).__init__(user_id=user_id, database_path=DATABASE_PATH)
        self._update()
    
    def _update(self):
        '''更新自己的属性'''
        super()._update()
        
        # 更新state
        t=self.read(STATE)
        # t = a:b|c:d
        if t == None:
            self.state = dict()
        else:
            self.state = self.str2Dict(t)
        
        time_now = datetime.now().replace(microsecond=0)
        self.state = {key: value for key, value in self.state.items() if self.state[key] > time_now}
        
        self.write(STATE, self.dict2Str(self.state))

    def giveState(self, state_name, hours:int = 0, minutes:int = 0, seconds:int = 0):
        # 查询 state_name 是否存在
        has_state = False
        state_table = pd.read_csv(STATE_TABLE_PATH, encoding="gb2312")
        for row in range(state_table.shape[0]):
            if state_table.at[row, ENGLISG_NAME] == state_name:
                has_state = True
                break
            
        if not has_state:
            return
        
        self.state[state_name] = datetime.now().replace(microsecond=0) + dt.timedelta(hours = hours, minutes = minutes, seconds = seconds)
        self.write(STATE, self.dict2Str(self.state))
    
    def exist(self, english_name) -> bool:
        '''判断用户是否存在状态'''
        # 格式1 状态:结束时间
        _exist = False
        for state_name in self.state:
            if state_name == english_name:
                _exist = True
                break
        return _exist
        
    @classmethod
    def getNamebyEnglishName(self, english_name) -> str:
        '''查询名称'''
        state_table = pd.read_csv(STATE_TABLE_PATH, encoding="gb2312")
        name = state_table.at[self.getIdByEnglishName(english_name=english_name), NAME]
        return name
    
    @classmethod
    def getIdByEnglishName(self, english_name) -> int|None:
        state_table = pd.read_csv(STATE_TABLE_PATH, encoding="gb2312")
        for i in range(state_table.shape[0]):
            if state_table.at[i, ENGLISG_NAME] == english_name:
                return i
        else:
            return None
    
    @classmethod
    def getDescribeByEnglishName(self, english_name) -> str:
        state_table = pd.read_csv(STATE_TABLE_PATH, encoding="gb2312")
        description = state_table.at[self.getIdByEnglishName(english_name=english_name), DESCRIPTION]
        msg = ""
        msg += f"\r\n{description}"
        return msg
    
    # 以下是辅助函数
    def str2Dict(self, s:str) -> dict[str, datetime]:
        '''将字符串 s="a+time1|b+time2" 变为字典 d={"a":time1, "b":time2} '''
        if not s:
            return dict()
        
        str_list = s.split("|") # ["a:123", "b:456"]
        d = dict() 
        
        for i in str_list:
            parts = i.split('+') # parts = ["a","123"]
            if len(parts) == 2:
                d[parts[0]] = datetime.strptime(parts[1], TIME_FORMAT)
        return d
    
    def dict2Str(self, d:dict) -> str:
        '''将字典 d={"a":123, "b":456} 变为 字符串 s="a+123|b+456" '''
        s = "|".join(f"{str(k)}+{str(v)}" for k, v in d.items())
        return s
    
    