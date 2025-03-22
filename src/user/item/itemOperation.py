from User import User
from pet import Pet
import pandas as pd

DATABASE_PATH = "./src/database/useritem.csv"

ITEM_TABLE_PATH = "./src/database/item_table.csv"

from item.item import Item

# 在此注册所有道具
from item.test_item import test_item
from item.expSaveBall import expSaveBall
ITEM_CLASS_MAPPING = {
    "test_item": test_item,
    "expSaveBall": expSaveBall,
}

class ItemOperation(User):
    def __init__(self, user_id:int):
        super(ItemOperation, self).__init__(user_id=user_id, database_path=DATABASE_PATH)
        self._update()
    
    def buy(self, name:str, num:int) -> str:
        '''购买道具'''
        msg = ""
        
        if num <=0: # 禁止购买0个道具
            return msg
        
        item_id = self.getIdbyName(name)
        if item_id == "":
            return msg
        
        item = Item(user_id=self.user_id, item_id=self.getIdbyName(name=name))
        name_in_useritem = Item.getNameinUseritembyId(item_id=self.getIdbyName(name=name))
        item_class = ITEM_CLASS_MAPPING.get(name_in_useritem, "")
        
        # 判断最大上限，道具不能超过最大上限
        if item.number + num > item.getMaxNumber():
            msg += f"该道具数量上限为{item.getMaxNumber()}，你已超上限"
            return msg
        
        p = Pet(self.user_id)
        total_price = item_class.getPrice()*num
        cry_enouth = p.hasCry(total_price)
        msg += p.useCry(total_price)
        if cry_enouth:
            msg += f"\r\n已购买{num}个{name}。"
            item.number += num
            item.write(item.getNameinUseritem(), item.number)
        
        return msg
    
    def use(self, name:str, num):
        '''使用物品，请在内部自行详细定义'''
        name_in_useritem = Item.getNameinUseritembyId(item_id=self.getIdbyName(name=name))
        item_class = ITEM_CLASS_MAPPING.get(name_in_useritem, "")
        son_item = item_class(user_id = self.user_id)
        msg = son_item.use(num)
        return msg
    
    def myitem(self) -> str:
        msg = "\r\n你的道具如下"
        for value in ITEM_CLASS_MAPPING.values():
            son_item = value(user_id=self.user_id)
            if son_item.number != 0:
                msg += f"\r\n- {son_item.getName()} x {son_item.number}"
        if msg == "\r\n你的道具如下":
            msg += "\r\n空空如也！"
        return msg

    @classmethod
    def describe(self, name:str) -> str:
        '''查询道具的描述'''
        name_in_useritem = Item.getNameinUseritembyId(item_id=self.getIdbyName(name=name))
        item_class = ITEM_CLASS_MAPPING.get(name_in_useritem, "")
        msg = item_class.descripe()
        return msg
    
    @classmethod
    def shop(self) -> str:
        msg = ""
        msg += "商店物品"
        for value in ITEM_CLASS_MAPPING.values():
            msg += f"\r\n- {value.getName()}：{value.getPrice()}水晶"
        return msg
    
    @classmethod
    def getIdbyName(self, name:str) -> int:
        '''查询道具在表中的名称'''
        item_table = pd.read_csv(ITEM_TABLE_PATH, encoding="gb2312")
        row_list = item_table[item_table['name']==name]
        print("row_list:", row_list)
        if row_list.empty:
            return ""
        return int(row_list.index[0])
    
    