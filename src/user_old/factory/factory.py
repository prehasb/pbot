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
CRY_PH = "cry_per_hour"
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
        
    def levelupFac(self) -> str:
        "扣除水晶，升级工厂，返回消息。若水晶不够，给出提示。"
        from user.pet import Pet
        msg = ""
        p = Pet(self.user_id)
        if p.crystal_num >= self.getFacLevelupCry():
            p.crystal_num -= self.getFacLevelupCry()
            self.factory_level += 1
            p.write(CRY_NUM, p.crystal_num)
            self.write(FAC_LEVEL, self.factory_level)
            msg = f'你成功升级了工厂，现在你的工厂等级为: {self.getFacName()}'
            expps = self.getFacrotyExpPs()
            if expps > 0:
                msg += f'\r\n每秒产出{expps}点经验'
            cryph = self.getFacrotyCryPh()
            if cryph > 0:
                msg += f'\r\n每小时产出{cryph}个水晶'
        else:
            msg = '你的水晶不够让工厂升级！'
        return msg
    
    def delayFactoryTime(self, days = 0, hours = 0, minutes = 0, seconds = 0) -> str:
        self.last_lookup_time += dt.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        self.write(LAST_LOOKUP_TIME, self.last_lookup_time)
    
    def updateExpandCry(self) -> str:
        '''取出经验和水晶，并根据存储的经验值，判断玛德琳是否可以升级'''
        msg = ""
        from user.state.stateOperator import stateOperator
        so = stateOperator(self.user_id)
        if so.exist("factoryStop"):
            msg += "工厂生产停滞中！"
            return msg
        
        from user.pet import Pet
        p = Pet(self.user_id)
        p.exp += self.getExpNum()
        p.crystal_num += self.getCryNum()
        
        
        if p.exp > p.getLevelUpExp()*10:
            msg += "\r\n你的玛德琳快饿死了！"
        
        exp_num = self.getExpNum()
        msg += f"\r\n你获得了{exp_num}经验值"
        cry_num = self.getCryNum()
        if cry_num != 0:
            msg += f"\r\n你获得了{cry_num}个冲刺水晶"
        
        # 执行升级
        msg += p.levelupPet()
        
        lookup_time = datetime.now().replace(microsecond=0)
        self.write(LAST_LOOKUP_TIME, lookup_time)
        p.write(PET_EXP, p.exp)
        p.write(CRY_NUM, p.crystal_num)
        self._update()
        return msg
    
    # 以下是get类型函数
    
    def getFacrotyExpPs(self, button_flag = True, eater_flag = True, double_flag = True) -> int:
        '''计算工厂每秒产生的经验值'''
        
        factory_table = pd.read_csv(FACTORY_TABLE_PATH, encoding="gb2312")
        expPs = factory_table.at[self.factory_level-1, EXP_PS]
        
        # 20250510添加：反转按钮，经验值与水晶反转
        #######################################################
        if button_flag:
            from item.reverseButton import reverseButton
            button = reverseButton(self.user_id)
            if button.state == 1:
                expPs = factory_table.at[self.factory_level-1, CRY_PH]
            
                # 20250418添加：宠物每升100级增加1水晶数量
                #######################################################
                from user.pet import Pet
                p = Pet(self.user_id)
                expPs += p.level//100
                #######################################################
                expPs = self.getFacrotyCryPh(button_flag=False)
        
        #######################################################
        
        # 20250323添加：经验吞噬者，经验值归零
        #######################################################
        if eater_flag:
            from item.expEater import expEater
            eater = expEater(self.user_id)
            if eater.state == 1:
                expPs = 0
        #######################################################
        
        # 20250627添加：翻倍
        #######################################################
        if double_flag:
            from user.state.stateOperator import stateOperator
            so = stateOperator(self.user_id)
            if so.exist("factoryDouble"):
                expPs *= 2
        #######################################################
        
        return int(expPs)
    
    # TODO 用装饰器重写
    def getFacrotyCryPh(self, steel_flag = True, button_flag = True, eater_flag = True, double_flag = True) -> int:
        '''计算工厂每小时产生的水晶数量'''
        
        factory_table = pd.read_csv(FACTORY_TABLE_PATH, encoding="gb2312")
        CryPh = int(factory_table.at[self.factory_level-1, CRY_PH])
        
        # 20250418添加：宠物每升100级增加1水晶数量
        #######################################################
        from user.pet import Pet
        p = Pet(self.user_id)
        CryPh += p.level//100
        #######################################################
        
        # 20250614添加：每持有1个黑钢，增加1水晶数量
        #######################################################
        if steel_flag:
            from item.darkmoonRuins.darksteel import darksteel
            steel = darksteel(self.user_id)
            CryPh += steel.number
        #######################################################
        
        # 20250510添加：反转按钮，经验值与水晶反转
        #######################################################
        if button_flag:
            from item.reverseButton import reverseButton
            button = reverseButton(self.user_id)
            if button.state == 1:
                CryPh = factory_table.at[self.factory_level-1, EXP_PS]
                CryPh = self.getFacrotyExpPs(button_flag=False, eater_flag=False)
        #######################################################
        
        # 20250323添加：经验吞噬者，水晶数量翻倍
        #######################################################
        if eater_flag:
            from item.expEater import expEater
            eater = expEater(self.user_id)
            if eater.state == 1:
                CryPh *= 2
        #######################################################
        
        # 20250627添加：翻倍
        #######################################################
        if double_flag:
            from user.state.stateOperator import stateOperator
            so = stateOperator(self.user_id)
            if so.exist("factoryDouble"):
                CryPh *= 2
        #######################################################
        
        return int(CryPh)
    
    # TODO 用装饰器重写
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
        from user.pet import Pet
        p = Pet(self.user_id)
        MAX_EXP_PL = 100
        max_save_exp += (p.level-1)*MAX_EXP_PL
        #######################################################
        
        return int(max_save_exp)
    
    def getOriginMaxSaveExp(self) -> int:
        '''查询原始最大存储经验'''
        factory_table = pd.read_csv(FACTORY_TABLE_PATH, encoding="gb2312")
        max_save_exp = factory_table.at[self.factory_level-1, MAX_SAVE_EXP]
        return int(max_save_exp)
    
    def getFacName(self) -> str:
        '''获取工厂名称'''
        fac_table = pd.read_csv(FACTORY_TABLE_PATH, encoding="gb2312")
        name = fac_table.at[self.factory_level-1, NAME]
        return name

    def getFacLevelupCry(self) -> int:
        factory_table = pd.read_csv(FACTORY_TABLE_PATH, encoding="gb2312")
        levelup_cry = int(factory_table.at[self.factory_level-1, LEVELUP_CRY])
        return levelup_cry
    
    def getExpNum(self) -> int:
        '''待领取的exp值'''
        from user.pet import Pet
        p = Pet(self.user_id)
        current_time = dt.datetime.now()
        time_difference = current_time - self.last_lookup_time
        second_difference = int(time_difference.total_seconds())
        if second_difference < 0 :
            second_difference = 0
        print(f"second_difference: {second_difference}")
        expPs = self.getFacrotyExpPs()
        
        total_exp = second_difference * expPs
        if total_exp > self.getMaxSaveExp():
            total_exp = self.getMaxSaveExp()
        
        # 超高经验值惩罚
        if p.exp > p.getLevelUpExp()*10:
            total_exp *= (p.getLevelUpExp()*10)/(p.exp)
            total_exp = int(total_exp)
        return total_exp
    
    def getCryNum(self) -> int:
        '''待领取的水晶数量'''
        current_time_hour = dt.datetime.now().replace(minute=0,second=0,microsecond=0)
        last_lookup_time_hour = self.last_lookup_time.replace(minute=0,second=0,microsecond=0)
        time_difference = current_time_hour - last_lookup_time_hour
        second_difference = time_difference.total_seconds()
        if second_difference < 0 :
            second_difference = 0
        hour_difference = int(second_difference//3600)
        cryPh = self.getFacrotyCryPh()
        return hour_difference * cryPh

class CalaulateFlag(object):
    
    def __init__(self):
        super(CalaulateFlag, self).__init__()
        