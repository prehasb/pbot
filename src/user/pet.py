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

IMAGE_PATH = "./src/database/image"

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_NAN = "2000-01-01 00:00:00"

class Pet(User):
    
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
        
        # 更新 
        # feeded_cry:int = None
        t=str(self.read(FEEDED_CRY))
        if str(t) == "nan":
            self.feeded_cry = 0
            self.write(FEEDED_CRY, self.feeded_cry)
        else:
            self.feeded_cry = int(float(t))
        
        
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

    def _getFacrotyCryPh(self) -> int:
        factory_table = pd.read_csv(FACTORY_TABLE_PATH, encoding="gb2312")
        CryPh = factory_table.at[self.factory_level-1, CRY_PS]
        return CryPh
        
    def getLevelUpExp(self) -> int:
        '''查询升级所需经验'''
        pet_table = pd.read_csv(PET_TABLE_PATH, encoding="gb2312")
        levelup_exp = pet_table.at[self.level-1, LEVELUP_EXP]
        return int(levelup_exp)

    def getLevelUpCry(self) -> int:
        '''查询升级所需水晶'''
        pet_table = pd.read_csv(PET_TABLE_PATH, encoding="gb2312")
        levelup_cry = int(float(pet_table.at[self.level-1, LEVELUP_CRY]))
        return levelup_cry
    
    def getMaxSaveExp(self) -> int:
        '''查询最大存储经验'''
        factory_table = pd.read_csv(FACTORY_TABLE_PATH, encoding="gb2312")
        max_save_exp = factory_table.at[self.factory_level-1, MAX_SAVE_EXP]
        return int(max_save_exp)

    def getName(self) -> str:
        '''获取宠物名称'''
        pet_table = pd.read_csv(PET_TABLE_PATH, encoding="gb2312")
        name = pet_table.at[self.level-1, NAME]
        return name

    def getImagePath(self) -> str:
        name = self.getName()
        image_path = os.path.abspath(IMAGE_PATH) +"\\" + name + ".png"
        if not os.path.exists(image_path):
            return None
        file_image_path = "file:///" + image_path
        print(f"imagepath: {file_image_path}")
        return file_image_path

    def getFacName(self) -> str:
        '''获取工厂名称'''
        fac_table = pd.read_csv(FACTORY_TABLE_PATH, encoding="gb2312")
        name = fac_table.at[self.factory_level-1, NAME]
        return name
    
    def giveCry(self, num) -> str:
        self.crystal_num += num
        self.write(CRY_NUM, self.crystal_num)
        return f"已发放{num}个水晶"
    
    def getExpNum(self) -> int:
        '''待领取的exp值'''
        current_time = dt.datetime.now()
        time_difference = current_time - self.last_lookup_time
        second_difference = int(time_difference.total_seconds())
        print(f"second_difference: {second_difference}")
        expPs = self._getFacrotyExpPs()
        
        total_exp = second_difference * expPs
        if total_exp > self.getMaxSaveExp():
            total_exp = self.getMaxSaveExp()
        return total_exp
    
    def getCryNum(self) -> int:
        '''待领取的水晶数量'''
        current_time_hour = dt.datetime.now().replace(minute=0,second=0,microsecond=0)
        last_lookup_time_hour = self.last_lookup_time.replace(minute=0,second=0,microsecond=0)
        time_difference = current_time_hour - last_lookup_time_hour
        second_difference = time_difference.total_seconds()
        hour_difference = int(second_difference//3600)
        cryPh = self._getFacrotyCryPh()
        return hour_difference * cryPh
    
    def getFacLevelupCry(self) -> int:
        factory_table = pd.read_csv(FACTORY_TABLE_PATH, encoding="gb2312")
        levelup_cry = int(factory_table.at[self.factory_level-1, LEVELUP_CRY])
        return levelup_cry
        
    def levelupFac(self) -> str:
        msg = ""
        if self.crystal_num >= self.getFacLevelupCry():
            self.crystal_num -= self.getFacLevelupCry()
            self.factory_level += 1
            self.write(CRY_NUM, self.crystal_num)
            self.write(FAC_LEVEL, self.factory_level)
            msg = f'你成功升级了工厂，现在你的工厂等级为: 冲刺水晶工厂lv{self.factory_level}'
            if self._getFacrotyExpPs()>0:
                msg += f'\r\n每秒产出{self._getFacrotyExpPs()}点经验'
            if self._getFacrotyCryPh()>0:
                msg += f'\r\n每小时产出{self._getFacrotyCryPh()}个水晶'
        else:
            msg = '你的水晶不够让工厂升级！'
        return msg
    
    def addExpbyJRRP(self, jrrp) -> str:
        add_exp = int(jrrp*0.01*(self.getLevelUpExp() - self.exp))
        min_exp = int(jrrp*0.001*(self.getLevelUpExp()))
        if add_exp < min_exp :
            add_exp = min_exp
        self.exp += add_exp
        self.write(PET_EXP, self.exp)
        msg = f"\r\n已领取{add_exp}点经验值！"
        msg += f"\r\n 当前玛德琳的经验值为{self.exp}/{self.getLevelUpExp()}点！"
        msg += self.levelupPet()
        return msg
    
    def feed(self, num:int) -> str:
        '''喂养num个水晶，多的退返'''
        msg = ""
        # self.getPetLevelupCry() = 2, num = 3, self.feeded_cry = 1
        # self.getPetLevelupCry() = 2, num = -1, self.feeded_cry = 1
        # self.getPetLevelupCry() = 2, num = 0, self.feeded_cry = 1
        feednum = 0
        
        if(self.crystal_num < num):
            msg += f"\r\n你没有{num}个水晶，你只有{self.crystal_num}个"
            return msg
        
        if self.getLevelUpCry()>0: # 玛德琳想吃的水晶数是正数
            if self.feeded_cry + num <= self.getLevelUpCry(): # 喂的水晶小于等于要吃的水晶
                feednum = num # feednum = ?, -1, 0
            if self.feeded_cry + num > self.getLevelUpCry(): # 喂的水晶大于要吃的水晶
                feednum = self.getLevelUpCry() - self.feeded_cry # feednum = 1, ?, ?
        
        if num <=0: # feednum = ?, -1, ?
            return f"ValueError: {feednum} is not a positive number."
            return f""
        
        self.feeded_cry += feednum
        self.crystal_num -= feednum
        if feednum <= 0:
            msg += "你的玛德琳不想吃水晶"
            return msg
        
        msg += f"\r\n已喂养{feednum}个水晶"
        
        msg += self.levelupPet()
        
        self.write(FEEDED_CRY, self.feeded_cry)
        self.write(CRY_NUM, self.crystal_num)
        
        return msg
    
    def canLevelUp(self) -> bool:
        '''查询升级条件'''
        levelup_exp = self.getLevelUpExp()
        levelup_cry = self.getLevelUpCry()
        if self.exp >= levelup_exp and self.feeded_cry >= levelup_cry:
            return True
        return False
        
    def levelupPet(self) -> str:
        '''按下升级按钮'''
        msg = ""
        leveluped = False
        get_cry_num = 0
        
        if self.canLevelUp():
            leveluped = True
        
        while self.canLevelUp():
            get_cry_num = 0
            
            self.exp -= self.getLevelUpExp() # 消耗经验值升级
            
            if self.getLevelUpCry() > 0: # 设置的水晶值为正数
                self.feeded_cry -= self.getLevelUpCry() # 消耗水晶升级
            
            if self.getLevelUpCry() < 0: # 设置的水晶值为负数
                get_cry_num = -self.getLevelUpCry()
            
            self.level += 1
            
            msg += f'\r\n你的玛德琳升级了！'
            
            if get_cry_num > 0:
                self.crystal_num += get_cry_num
                msg += f'升级时获得了{get_cry_num}个充能水晶。\r\n'
            
            msg += f"现在你的玛德琳为: lv{self.level} {self.getName()}"
            
            if self.feeded_cry < self.getLevelUpCry():
                msg += f'\r\n玛德琳想吃({self.feeded_cry}/{self.getLevelUpCry()})个充能水晶'

        if leveluped:
            self.write(PET_LEVEL, self.level)
            self.write(PET_EXP, self.exp)
            self.write(CRY_NUM, self.crystal_num)
            self.write(FEEDED_CRY, self.feeded_cry)
        
        return msg
    
    def updateExpandCry(self) -> str:
        '''取出经验和水晶，并根据存储的经验值，判断玛德琳是否可以升级'''
        msg = ""
        self.exp += self.getExpNum()
        self.crystal_num += self.getCryNum()
        lookup_time = datetime.now().replace(microsecond=0)
        # 执行升级
        msg += self.levelupPet()
        self.write(LAST_LOOKUP_TIME, lookup_time)
        self.write(PET_EXP, self.exp)
        self.write(CRY_NUM, self.crystal_num)
        self._update()
        return msg





