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

from item.item import Item

from item.itemRegistor import ITEM_CLASS_MAPPING

class ItemOperation(User):
    def __init__(self, user_id:int):
        super(ItemOperation, self).__init__(user_id=user_id, database_path=DATABASE_PATH)
        self._update()
    
    def buy(self, name:str, num:int) -> str:
        '''购买道具'''
        msg = ""
        
        if num <=0: # 禁止购买0个道具
            return msg
        
        if not self.exist(name):
            msg += f"不存在该物品[{name}]！"
            return msg
        
        # 获取子物品实例
        english_name = self.getEnglishNamebyName(name)
        id = self.getIdbyName(name)
        itemClass = ITEM_CLASS_MAPPING.get(english_name, Item)
        item_being_bought = itemClass(user_id=self.user_id)
        
        # 根据数据库，判断是否可购买
        if not item_being_bought.canBuy():
            msg += f"不可购买该物品[{name}]！"
            return msg
        
        # 根据数据库，判断最大上限，道具不能超过最大上限
        if item_being_bought.number + num > item_being_bought.getMaxNumber():
            msg += f"该道具数量上限为{item_being_bought.getMaxNumber()}，你已超上限"
            return msg
        
        # 花费水晶进行购买
        p = Pet(self.user_id)
        total_price = itemClass.getPrice()*num
        
        has_cryBool = p.hasCry(total_price)
        msg += p.useCry(total_price)
        
        if not has_cryBool:
            return msg
        
        msg += f"\r\n已购买{num}个{name}。"
        item_being_bought.number += num
        item_being_bought.write(item_being_bought.getNameinUseritem(), item_being_bought.number)
        
        return msg
    
    def use(self, name:str, num:int):
        '''使用物品，请在内部自行详细定义'''
        
        msg = ""
        
        if num <=0: # 禁止使用0个道具
            return msg
        
        if not self.exist(name):
            msg += f"不存在该物品[{name}]！"
            return msg
        
        english_name = self.getEnglishNamebyName(name)
        itemClass = ITEM_CLASS_MAPPING.get(english_name, Item)
        item_being_used = itemClass(user_id = self.user_id)
        
        if not item_being_used.canUse():
            msg = f"不可使用该物品[{item_being_used.getName()}]！"
            return msg
        
        msg = item_being_used.use(num)
        return msg
    
    def myitem(self) -> str:
        msg = "\r\n你的道具如下"
        for english_name in ITEM_CLASS_MAPPING.keys():
            id = self.getIdbyEnglishName(english_name)
            item_being_checked = ITEM_CLASS_MAPPING[english_name](user_id=self.user_id)
            if item_being_checked.number != 0:
                msg += f"\r\n- {item_being_checked.getName()} x {item_being_checked.number}"
        if msg == "\r\n你的道具如下":
            msg += "\r\n空空如也！"
        return msg
    
    def give(self, name:str, num:int = 1) -> str:
        '''
        name: 英文名称
        num: 数量
        '''
        from pet import Pet
        
        p = Pet(self.user_id)
        msg = ""
        add_msg = ""
        if not self.exist(name):
            msg += f"不存在该物品[{name}]！"
            return msg
        
        english_name = self.getEnglishNamebyName(name)
        item_class = ITEM_CLASS_MAPPING.get(english_name, Item)
        son_item = item_class(user_id=self.user_id)
        
        son_item.number += num
        if son_item.number > son_item.getMaxNumber():
            extra_num = son_item.number - son_item.getMaxNumber()
            cry = son_item.getPrice()//2
            add_msg = f"\r\n多余的{extra_num}个{son_item.getName()}转化为{cry*extra_num}数量水晶"
            p.addCry(cry*extra_num)
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
        msg += add_msg
        return msg
    
    @classmethod
    def specialName(self, name:str) -> bool:
        '''特殊名字开小灶，判断它存在'''
        
        if name[:5] == "水晶之心：": # name = "水晶之心：XXXX"
            return "水晶之心"
        return name
    
    @classmethod
    def exist(self, name:str) -> bool:
        '''查询数据库中是否存在名为name的道具'''
        
        # 特殊名字规则开个小灶
        name = self.specialName(name)
        english_name = self.getEnglishNamebyName(name)
        
        if english_name != None:
            return True
        
        return False
    
    @classmethod
    def describe(self, name:str) -> str:
        '''查询道具的描述'''
        msg = ""
        if not self.exist(name):
            msg += f"不存在该物品[{name}]！"
            return msg
        
        english_name = self.getEnglishNamebyName(name)
        itemClass = ITEM_CLASS_MAPPING.get(english_name, Item)
        msg = itemClass.describe()
        
        return msg
    
    @classmethod
    def shop(self) -> str:
        msg = ""
        msg += "商店物品"
        for itemClass in ITEM_CLASS_MAPPING.values():
            if itemClass.canBuy():
                msg += f"\r\n- {itemClass.getName()}：{itemClass.getPrice()}水晶"
        return msg
    
    @classmethod
    def getIdbyName(self, name:str) -> int|None:
        '''查询道具在item_table表中的名称'''
        item_table = pd.read_csv(ITEM_TABLE_PATH, encoding="gb2312")
        row_list = item_table[item_table[NAME]==name]
        if row_list.empty:
            return None
        return int(row_list.index[0])
    
    @classmethod
    def getIdbyEnglishName(self, name_in_useritem:str) -> int|None:
        '''查询道具在item_table表中的名称'''
        item_table = pd.read_csv(ITEM_TABLE_PATH, encoding="gb2312")
        row_list = item_table[item_table[NAME_IN_USERITEM]==name_in_useritem]
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
    
    @classmethod
    def getEnglishNamebyName(self, name:str) -> int|None:
        '''查询道具在表中的英文名称'''
        item_table = pd.read_csv(ITEM_TABLE_PATH, encoding="gb2312")
        row_list = item_table[item_table[NAME]==name]
        if row_list.empty:
            return None
        return item_table.at[int(row_list.index[0]), NAME_IN_USERITEM]
    
    