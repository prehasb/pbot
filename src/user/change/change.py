from pet import Pet
from user import User
import pandas as pd
from user.Global import Global
import nonebot
from nonebot import on_command
from .config import API_GROUP_ID
import math

GLOBAL_PATH = "./src/database/global.csv"
RATE_TOTAL_STRAWBERRY = "rate_total_strawberry"
RATE_TOTAL_CRYSTAL = "rate_total_crystal"


class Change(object):
    '''Change 兑换货币类'''
    data = dict()
    
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
    
    @classmethod
    def getTotalStrawberry(self) -> int:
        s = Global.read(RATE_TOTAL_STRAWBERRY)
        if s == None:
            s = 0
        return s
    
    @classmethod
    def getTotalCrystal(self) -> int:
        c = Global.read(RATE_TOTAL_CRYSTAL)
        if c == None:
            c = 0
        return c
    
    @classmethod
    def getCryNeededFor(self, stb:int) -> int:
        total_s = self.getTotalStrawberry()
        total_c = self.getTotalCrystal()
        cry_needed = math.ceil((total_c*stb)/(total_s-stb))
        return cry_needed
    
    @classmethod
    def getStbNeededFor(self, cry) -> int:
        s = self.getTotalStrawberry()
        c = self.getTotalCrystal()
        stb_needed = math.ceil(s*cry/(c-cry))
        return stb_needed
    
    def askForBuyStrawberry(self, stb) -> str:
        p = Pet(user_id=self.user_id)
        cry_needed = self.getCryNeededFor(stb)
        # 水晶不足
        if p.crystal_num < cry_needed:
            msg = f"你只有{p.crystal_num}个水晶，不足{cry_needed}个，无法兑换，"
            return msg
        # 存款不足
        if stb > self.getTotalStrawberry():
            msg = f"兑换的草莓数量过多，pbot没有这么多草莓！"
            return msg
        # 水晶足够
        msg = f"正在兑换草莓，预计花费{cry_needed}个水晶..."
        return msg
    
    def askForBuyStrawberryOK(self, stb) -> bool:
        p = Pet(user_id=self.user_id)
        cry_needed = self.getCryNeededFor(stb)
        # 水晶不足 or 存款不足
        if p.crystal_num < cry_needed or stb > self.getTotalStrawberry():
            return False
        else:
            return True
        
    
    def askForBuyCrystal(self, cry) -> str:
        stb_needed = self.getStbNeededFor(cry)
        # 存款不足
        if cry > self.getTotalCrystal():
            msg = f"兑换的水晶数量过多，pbot没有这么多水晶！"
            return msg
        msg = f"正在兑换水晶，预计花费{stb_needed}个草莓..."
        return msg
    
    def askForBuyCrystalOK(self, cry) -> bool:
        # 存款不足
        if cry > self.getTotalCrystal():
            return False
        else:
            return True
    
    '''
    查询草莓门槛（berry_check）
    调用方式：
        .berry_check <prefix> <user_id> <threshold> <command_prefix>(可选，默认为berry)
    返回：
        {prefix}{command_prefix}_check_finish {user_id} {threshold} {status}
    '''
    def sendBerryCheckText(self, threshold, command_prefix = "berry", prefix=","):
        command_text = f".berry_check {prefix} {self.user_id} {threshold} {command_prefix}"
        return command_text
    
    check = on_command("berry_check_finish")
    
    def processBerryCheck(self, threshold, status):
        msg = ""
        if status != 200:
            msg += "你的草莓不足，无法兑换"
            return msg
        
    
    '''更改草莓（berry_change）
    调用方式：
        .berry_check <prefix> <user_id> <number> <command_prefix>(可选，默认为berry)
    返回：
        {prefix}{command_prefix}_check_finish {user_id} {number} {status}
    '''
    def sendBerryChangeText(self, number : int, command_prefix = "berry", prefix=",") -> str:
        command_text = f".berry_change {prefix} {self.user_id} {number} {command_prefix}"
        return command_text
    
    change = on_command("berry_change_finish")
    
    def processBerryChange(self, stb, cry, status):
        msg = ""
        # 异常处理
        if status != 200:
            msg += "你正处于debuff中或草莓不足，无法兑换！"
            return msg
        
        g = Global()
        # 购买草莓
        if stb > 0:
            p = Pet(self.user_id)
            msg += f"已获得{stb}草莓。"
            msg += p.addCry(cry)
        # 购买水晶
        elif stb < 0:
            p = Pet(self.user_id)
            msg += p.addCry(cry)
            msg += f"已花费{-stb}草莓。"

        total_s = self.getTotalStrawberry() + stb
        total_c = self.getTotalCrystal() + cry
        g.write(RATE_TOTAL_STRAWBERRY, total_s)
        g.write(RATE_TOTAL_CRYSTAL, total_c)
        return msg
        
    @classmethod
    def isChangeFinished(self, user_id, status) -> bool:
        if status == 200:
            return True
        else:
            return False
    
    @classmethod
    def rate_text(self) -> str:
        msg = "当前汇率如下\r\n"
        s = self.getTotalStrawberry()
        c = self.getTotalCrystal()
        cps = c/s
        if c/s >1:
            msg += f"草莓:水晶 = 1:{int(100*cps)/100}"
        else:
            msg += f"水晶:草莓 = 1:{int(100/cps)/100}"
        return msg
    
    