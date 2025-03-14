from User import User
import datetime as dt
from datetime import datetime
import pandas as pd

PET_LEVEL = "pet_level"
PET_EXP = "pet_exp"
FAC_LEVEL = "factory_level"
CRY_NUM = "crystal_num"
LAST_LOOKUP_TIME = "last_lookup_time"

PET_TABLE_PATH = "./src/database/pet_table.csv"
LEVELUP_EXP = "levelup_exp"
NAME = "name"

FACTORY_TABLE_PATH = "./src/database/factory_table.csv"
EXP_PS = "exp_per_second"
CRY_PS = "cry_per_hour"


TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_NAN = "2000-01-01 00:00:00"

class Pet(User):
    
    level:int = None
    '''宠物等级'''
    exp:int = None
    '''宠物当前经验'''
    factory_level:int = None
    '''工厂当前等级'''
    crystal_num:int = None
    '''水晶当前数量'''
    last_lookup_time:datetime = datetime.strptime(TIME_NAN, TIME_FORMAT)
    
    def __init__(self, user_id : int):
        super(Pet, self).__init__(user_id=user_id)
        self._update()
    
    def _update(self):
        super()._update()
        '''更新自己的状态'''
        # 更新 level
        t=str(self.read(PET_LEVEL))
        if t == "nan":
            self.level = 1
            self.write(PET_LEVEL, self.level)
        else:
            self.level = int(float(t))
        
        # 更新 exp
        t=str(self.read(PET_EXP))
        if str(t) == "nan":
            self.exp = 0
            self.write(PET_EXP, self.exp)
        else:
            self.exp = int(float(t))
            
        # 更新 factory_level
        t=str(self.read(FAC_LEVEL))
        if str(t) == "nan":
            self.factory_level = 1
            self.write(FAC_LEVEL, self.factory_level)
        else:
            self.factory_level = int(float(t))
            
        # 更新 crystal_num
        t=str(self.read(CRY_NUM))
        if str(t) == "nan":
            self.crystal_num = 1
            self.write(CRY_NUM, self.crystal_num)
        else:
            self.crystal_num = int(float(t))
        
        # 更新 last_lookup_time (进行空检测)
        t = str(self.read(LAST_LOOKUP_TIME))
        if str(t) == "nan":
            self.last_lookup_time = dt.datetime.now().replace(microsecond=0)
            self.write(LAST_LOOKUP_TIME, self.last_lookup_time)
        else:
            self.last_lookup_time = datetime.strptime(t, TIME_FORMAT)
    
    def _getFacrotyExpPs(self) -> int:
        factory_table = pd.read_csv(FACTORY_TABLE_PATH, encoding="gb2312")
        expPs = factory_table.at[self.factory_level-1, EXP_PS]
        return expPs

    def getLevelUpExp(self) -> int:
        pet_table = pd.read_csv(PET_TABLE_PATH, encoding="gb2312")
        levelup_exp = pet_table.at[self.level-1, LEVELUP_EXP]
        return levelup_exp

    def getName(self) -> str:
        pet_table = pd.read_csv(PET_TABLE_PATH, encoding="gb2312")
        name = pet_table.at[self.level-1, NAME]
        return name

    def _getFacrotyCryPh(self) -> int:
        factory_table = pd.read_csv(FACTORY_TABLE_PATH, encoding="gb2312")
        CryPh = factory_table.at[self.factory_level-1, CRY_PS]
        return CryPh
    
    def getExpNum(self) -> int:
        current_time = dt.datetime.now()
        time_difference = current_time - self.last_lookup_time
        second_difference = int(time_difference.total_seconds())
        print(f"second_difference: {second_difference}")
        expPs = self._getFacrotyExpPs()
        return second_difference * expPs
    
    def getCryNum(self) -> int:
        current_time_hour = dt.datetime.now().replace(minute=0,second=0,microsecond=0)
        last_lookup_time_hour = self.last_lookup_time.replace(minute=0,second=0,microsecond=0)
        time_difference = current_time_hour - last_lookup_time_hour
        second_difference = time_difference.total_seconds()
        hour_difference = int(second_difference//3600)
        cryPh = self._getFacrotyExpPs()
        return hour_difference * cryPh
        
    def updateExpandCry(self) -> str:
        '''取出经验和水晶，并根据存储的经验值，判断玛德琳是否可以升级'''
        msg = ""
        new_exp = self.exp + self.getExpNum()
        new_crystal_num = self.crystal_num + self.getCryNum()
        lookup_time = datetime.now().replace(microsecond=0)
        # 是否可以升级
        leveluped = False
        while new_exp >= self.getLevelUpExp():
            new_exp -= self.getLevelUpExp()
            self.level += 1
            msg += f'你的玛德琳升级了！现在你的玛德琳为: lv{self.level} {self.getName()}\r\n'
            leveluped = True
        if leveluped:
            self.write(PET_LEVEL, self.level)
        self.write(PET_EXP, new_exp)
        self.write(CRY_NUM, new_crystal_num)
        self.write(LAST_LOOKUP_TIME, lookup_time)
        self._update()
        return msg
        
    
    
    
    
    