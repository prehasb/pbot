from User import User
from pet import Pet
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
CAN_BUY = "can_buy"

class ItemOperation(User):
    def __init__(self, user_id:int):
        super(ItemOperation, self).__init__(user_id=user_id, database_path=DATABASE_PATH)
        self._update()
    
    def mystate(self) -> str:
        msg = "\r\n你的附加状态如下"
        for value in STATE_CLASS_MAPPING.values():
            son_item = value(user_id=self.user_id)
            if son_item.number != 0:
                msg += f"\r\n- {son_item.getName()} x {son_item.number}"
        if msg == "\r\n你的附加状态如下":
            msg = "\r\n无附加状态"
        return msg
    
    def give(self, name:str, num:int) -> str:
        
        msg = ""
        if not self.exist(name):
            msg += f"不存在该物品[{name}]！"
            return msg
        
        name_in_useritem = Item.getNameinUseritembyId(item_id=self.getIdbyName(name=name))
        item_class = ITEM_CLASS_MAPPING.get(name_in_useritem, Item)
        son_item = item_class(user_id=self.user_id)
        
        son_item.number += num
        if son_item.number > son_item.getMaxNumber():
            son_item.number = son_item.getMaxNumber()

        if son_item.number < 0:
            son_item.number = 0
        
        son_item.write(son_item.getNameinUseritem(), son_item.number)
        
        gain_text = "获得"
        show_num = num
        if num < 0:
            gain_text = "失去"
            show_num = -num
        
        msg += f"\r\n已{gain_text}{show_num}个{name}，现在你有{son_item.number}个{name}"
        return msg
    
    
    @classmethod
    def exist(self, name:str) -> bool:
        '''查询数据库中是否存在名为name的道具'''
        item_id = self.getIdbyName(name)
        if item_id == None:
            return False
        return True
    
    @classmethod
    def describe(self, name:str) -> str:
        '''查询道具的描述'''
        msg = ""
        if not self.exist(name):
            msg += f"不存在该物品[{name}]！"
            return msg
        
        name_in_useritem = Item.getNameinUseritembyId(item_id=self.getIdbyName(name=name))
        
        item_class = ITEM_CLASS_MAPPING.get(name_in_useritem, Item)
        msg = item_class.describe()
        return msg
    
    @classmethod
    def shop(self) -> str:
        msg = ""
        msg += "商店物品"
        for value in ITEM_CLASS_MAPPING.values():
            if value.canBuy():
                msg += f"\r\n- {value.getName()}：{value.getPrice()}水晶"
        return msg
    
    @classmethod
    def getIdbyName(self, name:str) -> int|None:
        '''查询道具在表中的名称'''
        item_table = pd.read_csv(ITEM_TABLE_PATH, encoding="gb2312")
        row_list = item_table[item_table[NAME]==name]
        if row_list.empty:
            return None
        return int(row_list.index[0])
    
    @classmethod
    def getNamebyNameInUseritem(self, name_in_useritem:str) -> int|None:
        '''查询道具在表中的名称'''
        item_table = pd.read_csv(ITEM_TABLE_PATH, encoding="gb2312")
        row_list = item_table[item_table[NAME_IN_USERITEM]==name_in_useritem]
        if row_list.empty:
            return None
        return item_table.at[int(row_list.index[0]), NAME]
    
    