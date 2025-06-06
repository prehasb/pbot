﻿from User import User
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
MAP = "map"

IMAGE_PATH = "./src/database/image"

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_NAN = "2000-01-01 00:00:00"

# 重构，pet和factory分开

class Pet(User):
    '''Pet宠物类'''
    
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
        super(Pet, self).__init__(user_id=user_id)
        self._update()
    
    def _update(self):
        '''更新自己的状态'''
        super()._update()
        
        # 更新mode
        t=self.read(MAP)
        if t == None:
            self.map = "default"
            self.write(PET_LEVEL, self.map)
        else:
            self.map = t
        
        # 更新 level
        # 原："352.0" 新："default:352"
        t=self.read(PET_LEVEL)
        if t == None:
            self.level = 1
            self.write(PET_LEVEL, self.level)
        else:
            self.level = int(float(t))
        
        # 更新 exp
        # 原："352.0" 新："default:352"
        t=self.read(PET_EXP)
        if t == None:
            self.exp = 0
            self.write(PET_EXP, self.exp)
        else:
            self.exp = int(float(t))
        
        # 更新 
        # feeded_cry:int = None
        t=self.read(FEEDED_CRY)
        if t == None:
            self.feeded_cry = 0
            self.write(FEEDED_CRY, self.feeded_cry)
        else:
            self.feeded_cry = int(float(t))
        
        # 更新 factory_level
        t=self.read(FAC_LEVEL)
        if t == None:
            self.factory_level = 1
            self.write(FAC_LEVEL, self.factory_level)
        else:
            self.factory_level = int(float(t))
            
        # 更新 crystal_num
        t=self.read(CRY_NUM)
        if t == None:
            self.crystal_num = 1
            self.write(CRY_NUM, self.crystal_num)
        else:
            self.crystal_num = int(float(t))
        
        # 更新 last_lookup_time (进行空检测)
        t = self.read(LAST_LOOKUP_TIME)
        if t == None:
            self.last_lookup_time = dt.datetime.now().replace(microsecond=0)
            self.write(LAST_LOOKUP_TIME, self.last_lookup_time)
        else:
            self.last_lookup_time = datetime.strptime(t, TIME_FORMAT)
    
    def canLevelUp(self) -> bool:
        '''查询升级条件'''
        levelup_exp = self.getLevelUpExp()
        levelup_cry = self.getLevelUpCry()
        if self.exp >= levelup_exp and self.feeded_cry >= levelup_cry:
            return True
        return False
        
    def levelupPet(self) -> str:
        '''按下升级按钮，累计升级，返回升级提示。不满足升级条件，则不返回任何提示。'''
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
    
    def addExp(self, exp) -> str:
        self.exp += exp
        if self.exp < 0:
            self.exp = 0
        self.write(PET_EXP, self.exp)
        
        show_exp = exp
        gain_text = "获得"
        if exp < 0:
            show_exp = -exp
            gain_text = "失去"
        
        msg = f"\r\n已{gain_text}{show_exp}点经验，现在你有{self.exp}点经验。"
        msg += self.levelupPet()
        return msg
    
    def addCry(self, cry) -> str:
        self.crystal_num += cry
        if self.crystal_num < 0:
            self.crystal_num = 0
        self.write(CRY_NUM, self.crystal_num)
        
        show_cry = cry
        gain_text = "获得"
        if cry < 0:
            show_cry = -cry
            gain_text = "失去"
        
        msg = f"\r\n已{gain_text}{show_cry}点水晶，现在你有{self.crystal_num}个水晶。"
        return msg
    
    def hasCry(self, num) ->bool:
        if self.crystal_num >= num:
            return True
        else:
            return False
        
    def useCry(self, num) -> str:
        if not self.hasCry(num):
            msg = f"你没有足够的水晶！你只有{self.crystal_num}个"
            return msg
        cry_before = self.crystal_num
        self.crystal_num -= num
        self.write(CRY_NUM, self.crystal_num)
        msg = f"\r\n已使用{num}个水晶，还剩{self.crystal_num}个"
        return msg
        
    def levelupFac(self) -> str:
        "扣除水晶，升级工厂，返回消息。若水晶不够，给出提示。"
        msg = ""
        if self.crystal_num >= self.getFacLevelupCry():
            self.crystal_num -= self.getFacLevelupCry()
            self.factory_level += 1
            self.write(CRY_NUM, self.crystal_num)
            self.write(FAC_LEVEL, self.factory_level)
            msg = f'你成功升级了工厂，现在你的工厂等级为: 冲刺水晶工厂lv{self.factory_level}'
            expps = self.getFacrotyExpPs()
            if expps > 0:
                msg += f'\r\n每秒产出{expps}点经验'
            cryph = self.getFacrotyCryPh()
            if cryph > 0:
                msg += f'\r\n每小时产出{cryph}个水晶'
        else:
            msg = '你的水晶不够让工厂升级！'
        return msg
    
    def addExpbyJRRP(self, jrrp:int) -> str:
        '''根据jrrp值增加exp'''
        # add_exp = int(jrrp*0.01*(self.getLevelUpExp()))*2
        add_exp = int(jrrp*0.01*self.getOriginMaxSaveExp())
        # min_exp = int(jrrp*0.001*(self.getLevelUpExp())*2)
        # if add_exp < min_exp :
        #     add_exp = min_exp
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
        
        if num <= 0: # feednum = ?, -1, ?
            # return f"ValueError: {feednum} is not a positive number."
            return f""
        
        if(self.crystal_num < num):
            msg += f"\r\n你没有{num}个水晶，你只有{self.crystal_num}个"
            return msg
        
        if self.getLevelUpCry()>0: # 玛德琳想吃的水晶数是正数
            if self.feeded_cry + num <= self.getLevelUpCry(): # 喂的水晶小于等于要吃的水晶
                feednum = num # feednum = ?, -1, 0
            if self.feeded_cry + num > self.getLevelUpCry(): # 喂的水晶大于要吃的水晶
                feednum = self.getLevelUpCry() - self.feeded_cry # feednum = 1, ?, ?
        
        if ((feednum == 0 or self.feeded_cry >= self.getLevelUpCry()) and num > 0):
            msg += "你的玛德琳不想吃水晶"
            return msg
        
        self.feeded_cry += feednum
        self.crystal_num -= feednum
        
        msg += f"\r\n已喂养{feednum}个水晶"
        
        msg += self.levelupPet()
        
        self.write(FEEDED_CRY, self.feeded_cry)
        self.write(CRY_NUM, self.crystal_num)
        
        return msg
    
    # 以下是get类型函数
    
    def getFacrotyExpPs(self) -> int:
        '''计算工厂每秒产生的经验值'''
        
        factory_table = pd.read_csv(FACTORY_TABLE_PATH, encoding="gb2312")
        expPs = factory_table.at[self.factory_level-1, EXP_PS]
        
        # 20250323添加：经验吞噬者，经验值归零
        #######################################################
        from item.expEater import expEater
        eater = expEater(self.user_id)
        if eater.state == 1:
            expPs = 0
        #######################################################
        
        return int(expPs)
    
    def getFacrotyCryPh(self) -> int:
        '''计算工厂每小时产生的水晶数量'''
        
        factory_table = pd.read_csv(FACTORY_TABLE_PATH, encoding="gb2312")
        CryPh = int(factory_table.at[self.factory_level-1, CRY_PS])
        
        # 20250418添加：宠物每升100级增加1水晶数量
        #######################################################
        CryPh += self.level//100
        #######################################################
        
        # 20250323添加：经验吞噬者，水晶数量翻倍
        #######################################################
        from item.expEater import expEater
        eater = expEater(self.user_id)
        if eater.state == 1:
            CryPh *= 2
        #######################################################
        
        
        return int(CryPh)
        
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
        # max_save_exp = factory_table.at[self.factory_level-1, MAX_SAVE_EXP]*20 # 20250407关服补偿
        
        # 20250322添加：经验存储球
        #######################################################
        from item.expSaveBall import expSaveBall
        ball = expSaveBall(self.user_id)
        max_save_exp += ball.getAddMaxExp()
        #######################################################
        
        # 20250418添加：宠物每升一级增加经验值上限
        #######################################################
        MAX_EXP_PL = 100
        max_save_exp += (self.level-1)*MAX_EXP_PL
        #######################################################
        
        return int(max_save_exp)
    
    def getOriginMaxSaveExp(self) -> int:
        '''查询原始最大存储经验'''
        factory_table = pd.read_csv(FACTORY_TABLE_PATH, encoding="gb2312")
        max_save_exp = factory_table.at[self.factory_level-1, MAX_SAVE_EXP]
        return int(max_save_exp)
    
    @classmethod
    def getNamebyLevel(self, level:int) -> str:
        '''获取宠物名称'''
        pet_table = pd.read_csv(PET_TABLE_PATH, encoding="gb2312")
        name = pet_table.at[level-1, NAME]
        return name

    def getName(self) -> str:
        '''获取宠物名称'''
        return self.getNamebyLevel(level=self.level)
    
    @classmethod
    def getImagePathbyLevel(self, level:int) -> str:
        '''获取宠物图片路径'''
        name = self.getNamebyLevel(level=level)
        image_path = os.path.abspath(IMAGE_PATH) +"\\" + name + ".png"
        if not os.path.exists(image_path):
            return None
        file_image_path = "file:///" + image_path
        # print(f"imagepath: {file_image_path}")
        return file_image_path
    
    def getImagePath(self) -> str:
        '''获取宠物图片路径'''
        return self.getImagePathbyLevel(level=self.level)

    def getFacName(self) -> str:
        '''获取工厂名称'''
        fac_table = pd.read_csv(FACTORY_TABLE_PATH, encoding="gb2312")
        name = fac_table.at[self.factory_level-1, NAME]
        return name

    def getExpNum(self) -> int:
        '''待领取的exp值'''
        current_time = dt.datetime.now()
        time_difference = current_time - self.last_lookup_time
        second_difference = int(time_difference.total_seconds())
        print(f"second_difference: {second_difference}")
        expPs = self.getFacrotyExpPs()
        
        total_exp = second_difference * expPs
        if total_exp > self.getMaxSaveExp():
            total_exp = self.getMaxSaveExp()
        
        # 超高经验值惩罚
        if self.exp > self.getLevelUpExp()*10:
            total_exp *= (self.getLevelUpExp()*10)/(self.exp)
            total_exp = int(total_exp)
        return total_exp
    
    def getCryNum(self) -> int:
        '''待领取的水晶数量'''
        current_time_hour = dt.datetime.now().replace(minute=0,second=0,microsecond=0)
        last_lookup_time_hour = self.last_lookup_time.replace(minute=0,second=0,microsecond=0)
        time_difference = current_time_hour - last_lookup_time_hour
        second_difference = time_difference.total_seconds()
        hour_difference = int(second_difference//3600)
        cryPh = self.getFacrotyCryPh()
        return hour_difference * cryPh
    
    def getFacLevelupCry(self) -> int:
        factory_table = pd.read_csv(FACTORY_TABLE_PATH, encoding="gb2312")
        levelup_cry = int(factory_table.at[self.factory_level-1, LEVELUP_CRY])
        return levelup_cry
        



