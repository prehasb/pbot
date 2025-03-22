﻿from User import User
import pandas as pd

DATABASE_PATH = "./src/database/useritem.csv"

ITEM_TABLE_PATH = "./src/database/item_table.csv"
ITEM_ID = "item_id"
NAME = "name"
PRICE = "price"
MAX_NUMBER = "max_number"
NAME_IN_USERITEM = "name_in_useritem"
HAS_STATE = "has_state"
CAN_USE = "can_use"

class Item(User):
    '''item抽象类'''
    
    item_id:int
    '''物品id'''
    
    def __init__(self, user_id:int, item_id:int):
        super(Item, self).__init__(user_id=user_id, database_path=DATABASE_PATH)
        self.item_id = item_id
        self._update()
    
    def _update(self):
        '''更新自己的状态'''
        super()._update()
        name_in_useritem = self.getNameinUseritem()
        t=str(self.read(name_in_useritem))
        if t == "nan":
            self.number = 0
            self.write(name_in_useritem, 0)
        else:
            self.number = int(float(t))
        
        if not self.hasState():
            return
        
        state_column = self.getStateNameinUseritem()
        t=str(self.read(state_column))
        if t == "nan":
            self.state = 0
            self.write(state_column, 0)
        else:
            self.state = int(float(t))
        
    def isEnough(self, num) -> bool:
        '''判断物品是否足够num个'''
        if self.number >= num:
            return True
        else:
            return False
        
    def use(self, num) -> str:
        msg = ""
        
        if num <= 0:
            return msg
        
        if not self.isEnough(num):
            msg = f"你没有{num}个道具，你只有{self.number}个"
            return msg
        
        self.number -= num
        self.write(self.getNameinUseritem(), self.number)
        
        msg = f"已使用{num}个{self.getName()}，还剩{self.number}个。\r\n"
        
        return msg
    
    def changeState(self, state:int) -> str:
        msg = ""
        if self.state == 0 or state > self.state: # 不存在状态或超出最大状态
            return msg
        
        self.state = state
        self.write(self.getStateNameinUseritem(), state)
        msg += f"已改变状态为：{self.getStateName(state)}"
    
    @classmethod
    def getName(self) -> str:
        '''查询道具名称'''
        item_table = pd.read_csv(ITEM_TABLE_PATH, encoding="gb2312")
        name = item_table.at[self.item_id, NAME]
        return name
    
    @classmethod
    def getNameinUseritembyId(self, item_id) -> str:
        '''查询道具在表中的名称'''
        item_table = pd.read_csv(ITEM_TABLE_PATH, encoding="gb2312")
        name_in_useritem = item_table.at[item_id, NAME_IN_USERITEM]
        return name_in_useritem
    
    def getNameinUseritem(self) -> str:
        '''查询道具在表中的名称'''
        name_in_useritem = self.getNameinUseritembyId(self.item_id)
        return name_in_useritem
    
    def getStateNameinUseritem(self) -> str:
        return self.getNameinUseritem() + "_state"
    
    def getStateName(self, state) -> str:
        '''物品状态对应名称，请在内部定义'''
        pass
    
    def getMaxNumber(self) -> int:
        '''查询道具的最大数量'''
        item_table = pd.read_csv(ITEM_TABLE_PATH, encoding="gb2312")
        max_number = int(item_table.at[self.item_id, MAX_NUMBER])
        return max_number
    
    def isCanUse(self) -> bool:
        '''查询道具是否可以使用'''
        item_table = pd.read_csv(ITEM_TABLE_PATH, encoding="gb2312")
        can_use = bool(item_table.at[self.item_id, CAN_USE])
        return can_use
    
    def hasState(self) -> bool:
        '''查询道具是否具有状态'''
        item_table = pd.read_csv(ITEM_TABLE_PATH, encoding="gb2312")
        has_state = bool(item_table.at[self.item_id, HAS_STATE])
        return has_state
    
    @classmethod
    def getPrice(self) -> bool:
        '''查询道具价格'''
        item_table = pd.read_csv(ITEM_TABLE_PATH, encoding="gb2312")
        price = int(item_table.at[self.item_id, PRICE])
        return price
    
    @classmethod
    def describe(self) -> str:
        msg = ""
        msg += f"\r\n暂无该道具{self.getName}的描述"
        return msg

    
    
    