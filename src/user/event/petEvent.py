import pandas as pd
import datetime as dt
from datetime import datetime
import random as rd
import os

from User import User
from item.item import Item
from item.itemOperation import ItemOperation
# from item.itemRegistor import ITEM_CLASS_MAPPING

NEXT_EVENT_TIME = "next_event_time"
LAST_EVENT_ID = "last_event_id"

IMAGE_PATH = "./src/database/eventimage"

EVENT_TABLE_PATH = "./src/database/event_table.csv"
EVENT_ID = "event_id"
DESCRIPTION = "description"
MIN_LEVEL = "min_level"
MAX_LEVEL = "max_level"
P = "priority"
EXP = "exp"
CRY = "cry"
NEXT_TIME = "next_time"
IS_FIRST_EVENT = "is_first_event"
NEXT_EVENT = "next_event"
CHOOSE = "choose"
ITEM = "item"

NT_int = 30
# NT_int = 0

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_NAN = "2000-01-01 00:00:00"

class petEvent(User):
    '''pet event事件抽象类'''
    
    def __init__(self, user_id:int):
        super(petEvent, self).__init__(user_id=user_id)
        self._update()
    
    def _update(self):
        '''更新自己的状态'''
        super()._update()
        
        # 更新 next_event_time (进行空检测)
        t = self.read(NEXT_EVENT_TIME)
        if t == None:
            self.next_event_time = dt.datetime.now().replace(microsecond=0)
            self.write(NEXT_EVENT_TIME, self.next_event_time)
        else:
            self.next_event_time = datetime.strptime(t, TIME_FORMAT)
            
        # 更新 next_event_time (进行空检测)
        t = self.read(NEXT_EVENT_TIME)
        if t == None:
            self.next_event_time = dt.datetime.now().replace(microsecond=0)
            self.write(NEXT_EVENT_TIME, self.next_event_time)
        else:
            self.next_event_time = datetime.strptime(t, TIME_FORMAT)
        
        # 更新 last_event_id (进行空检测)
        t = self.read(LAST_EVENT_ID)
        if t == None:
            self.last_event_id = 0
            self.write(NEXT_EVENT_TIME, self.last_event_id)
        else:
            self.last_event_id = int(t)
    
    def canActivate(self) -> bool:
        now_time = datetime.now()
        if now_time < self.next_event_time:
            return False
        return True
    
    def cantActivateText(self) -> str:
        msg = ""
        msg += "\r\n你的玛德琳还没有给你寄信！"
        msg += "\r\n你记得上次收信的时间是："
        next_time = self.readEventTablebyID(self.last_event_id, NEXT_TIME)
        last_time = self.next_event_time - dt.timedelta(minutes=next_time)
        msg += str(last_time)
        return msg
    
    def activate(self) -> str:
        '''激活事件'''
        msg = ""
        
        self.event_id = self.pickNextEvent()
        
        if self.event_id == 0:
            self.event_id = self.pickRandomEvent()
        
        msg += "\r\n你收到了来自旅行中的玛德琳的一封信："
        
        msg += self.getDescription()
        
        from pet import Pet
        p = Pet(user_id=self.user_id)
        
        exp = self.getExp()
        if not exp == 0:
            msg += p.addExp(exp)
            
        cry = self.getCry()
        if not cry == 0:
            msg += p.addCry(cry)
        
        d = self.getItemDict()
        
        for name_in_useritem in d.keys():
            if d[name_in_useritem] != 0:
                num = d[name_in_useritem]
                name = ItemOperation.getNamebyNameInUseritem(name_in_useritem)
                io = ItemOperation(user_id=self.user_id)
                msg += io.give(name, num)
        
        self.write(NEXT_EVENT_TIME, self.getNextTime())
        self.write(LAST_EVENT_ID, self.event_id)
        
        return msg
    
    def getImagePATH(self) -> str:
        image_path = os.path.abspath(IMAGE_PATH) +"\\" + str(self.event_id) + ".png"
        if not os.path.exists(image_path):
            image_path = os.path.abspath(IMAGE_PATH) +"\\" + str(self.event_id) + ".jpg"
            if not os.path.exists(image_path):
                return None
        file_image_path = "file:///" + image_path
        return file_image_path
    
    @classmethod
    def getFirstEventDict(self) -> dict:
        '''获取可能的首次事件的字典:{id:priority}'''
        event_table = pd.read_csv(EVENT_TABLE_PATH, encoding="gb2312")
        d = dict()
        for id in range(event_table.shape[0]):
            p = event_table.at[id, P]
            if str(p) == "nan":
                p = 0
            p = int(p)
            first = event_table.at[id, IS_FIRST_EVENT]
            if str(first) == "nan":
                first = True
            first = bool(first)
            if p != 0 and first == True:
                d[id] = event_table.at[id, P]
        
        return d
    
    @classmethod
    def pickRandomEvent(self) -> int:
        '''根据权重按概率选择事件'''
        
        d = self.getFirstEventDict()
        event_id = self.pickRandomIDinDict(d)
        
        return event_id
    
    def getDescription(self) -> str:
        description = str(self.readEventTable(DESCRIPTION))
        return description
    
    def getNextTime(self) -> datetime:
        next_time = self.readEventTable(NEXT_TIME)
        if next_time == 0:
            next_time = NT_int
        next_time = datetime.now().replace(microsecond=0) + dt.timedelta(minutes=next_time)
        return next_time
    
    def getMinLevel(self) -> int:
        min_level = self.readEventTable(MIN_LEVEL)
        return int(min_level)
    
    def getMaxLevel(self) -> int:
        max_level = self.readEventTable(MAX_LEVEL)
        if max_level == 0:
            return 9999999999999
        return int(max_level)
    
    def getExp(self) -> int:
        '''获取经验值'''
        exp = self.readEventTable(EXP)
        return int(exp)

    def getCry(self) -> int:
        cry = self.readEventTable(CRY)
        return int(cry)
    
    def getItemDict(self) -> dict[str, int]:
        '''获取道具与其对应的字典:{name_in_useritem:number}'''
        item_str:str = self.readEventTable(NEXT_TIME)
        if item_str == 0:
            return dict()
        
        item_str_list = item_str.split("|") #["test_item:5", "expSaveBall:2"]
        item_dict = dict()
        
        for i in item_str_list:
            parts = i.split(':') # parts = ["test_item","5"]
            if len(parts) == 2:
                item_dict[parts[0]] = int(parts[1])
        return item_dict
    
    @classmethod
    def isFirstEventbyId(self, id) -> bool:
        event_table = pd.read_csv(EVENT_TABLE_PATH, encoding="gb2312")
        first_event = event_table.at[id, IS_FIRST_EVENT]
        if str(first_event) == "nan":
            return True
        return bool(first_event)
    
    @classmethod
    def getPbyID(self, id:int) -> int:
        event_table = pd.read_csv(EVENT_TABLE_PATH, encoding="gb2312")
        p = event_table.at[id, P]
        if str(p) == "nan":
            return 0
        return p
    
    def getNextEventDict(self) -> dict:
        '''获取可能的下一个事件字典:{id:priority}'''
        event_table = pd.read_csv(EVENT_TABLE_PATH, encoding="gb2312")
        next_event = self.readEventTablebyID(self.last_event_id, NEXT_EVENT) # 3|4|5 或 nan
        if next_event == 0:
            return dict()
        
        next_event_list = [int(x) for x in next_event.split("|")] #[3,4,5]
        next_event_dict = dict()
        for id in next_event_list:
            p = event_table.at[id, P]
            if p == "nan":
                p = 0
            p = int(p)
            if p != 0:
                next_event_dict[id] = p
        return next_event_dict #{3:500,4:400,5:100}
    
    def pickNextEvent(self) -> int:
        next_event_dict = self.getNextEventDict()
        if not next_event_dict:
            return 0
        event_id = self.pickRandomIDinDict(next_event_dict)
        return event_id
    
    @classmethod
    def pickRandomIDinDict(self, d:dict) -> int:
        '''通过字典的权重随机选择一个id，若表为空，返回0'''
        # 数据格式：d[id, priotiry] = {1:1, 5:1, 10:2, 11:1}
        
        sum_p = 0
        for id in d.keys():
            sum_p += d[id] # sum_p = 5
        
        rd.seed()
        random_number = rd.randint(1, sum_p) # randint=2
        event_id = 0
        for id in d.keys():
            if random_number <= d[id]: # 1: randint = 2, 2:randing = 1
                event_id = id # 2 event_id = 5
                break
            random_number -= d[id] #1: randing = 1
        
        return event_id
    
    @classmethod
    def readEventTablebyID(self, id, column):
        event_table = pd.read_csv(EVENT_TABLE_PATH, encoding="gb2312")
        var = event_table.at[id, column]
        if str(var) == "nan":
            return 0
        return var
    
    def readEventTable(self, column):
        return self.readEventTablebyID(self.event_id, column)
    
    def positive(self, num:int) -> int:
        if num > 0:
            return 1
        if num < 0:
            return -1
        return 0
    