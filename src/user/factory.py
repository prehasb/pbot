from User import User
import datetime as dt
from datetime import datetime
import pandas as pd
import os

PET_LEVEL = "pet_level"
PET_EXP = "pet_exp"
FAC_LEVEL = "factory_level"
CRY_NUM = "crystal_num"
LAST_LOOKUP_TIME = "last_lookup_time"
FEEDED_CRY = "feeded_cry"

PET_TABLE_PATH = "./src/database/pet_table.csv"
NAME = "name"
LEVELUP_EXP = "levelup_exp"
LEVELUP_CRY = "levelup_cry"

FACTORY_TABLE_PATH = "./src/database/factory_table.csv"
LEVELUP_CRY = "levelup_cry"
EXP_PS = "exp_per_second"
CRY_PS = "cry_per_hour"
MAX_SAVE_EXP = "max_save_exp"
MODE = "mode"

IMAGE_PATH = "./src/database/image"

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_NAN = "2000-01-01 00:00:00"

class Factory(User):
    '''Factory工厂类'''
    
    level:int = None
    '''宠物等级'''
    exp:int = None
    '''宠物当前经验'''
    feeded_cry:int = None
    '''宠物已食用水晶'''
    factory_level:int = None
    '''工厂当前等级'''
    crystal_num:int = None
    '''水晶当前数量'''
    map:str = None
    '''水晶当前数量'''
    
    last_lookup_time:datetime = datetime.strptime(TIME_NAN, TIME_FORMAT)
    
    def __init__(self, user_id : int):
        super(Factory, self).__init__(user_id=user_id)
        self._update()
    
    def _update(self):
        '''更新自己的状态'''
        super()._update()
        
        # 更新 factory_level
        t=self.read(FAC_LEVEL)
        if t == None:
            self.factory_level = 1
            self.write(FAC_LEVEL, self.factory_level)
        else:
            self.factory_level = int(float(t))
        
        # 更新 last_lookup_time (进行空检测)
        t = self.read(LAST_LOOKUP_TIME)
        if t == None:
            self.last_lookup_time = dt.datetime.now().replace(microsecond=0)
            self.write(LAST_LOOKUP_TIME, self.last_lookup_time)
        else:
            self.last_lookup_time = datetime.strptime(t, TIME_FORMAT)
    