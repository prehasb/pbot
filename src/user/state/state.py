from User import User
import pandas as pd

DATABASE_PATH = "./src/database/database.csv"
STATE_ENDTIME = "state_end_time"

STATE_TABLE_PATH = "./src/database/state_table.csv"
STATE_ID = "state_id"
ENGLISG_NAME = "english_name"
NAME = "name"

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
        name_in_useritem = self.getEnglishNamebyId(self.state_id)
        return name_in_useritem
    
    @classmethod
    def describe(self) -> str:
        msg = ""
        msg += f"\r\n暂无该状态{self.getName()}的描述"
        return msg

    
    
    