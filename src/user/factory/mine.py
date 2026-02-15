from User import User
import datetime as dt
from datetime import datetime
import pandas as pd

from user.pet import Pet

DATABASE_PATH = "./src/database/minedata.csv"
USER_ID = "user_id"
STONENAME = "stonename"
LEVEL = "level"
TEMPURATURE = "tempurature"
ACTIVITY = "activity"
STORAGE = "storage"

STONE_TABLE = "./src/database/stone_table.csv"
PRIORITY = "priority"
ADD_TEMPURATURE = "add_tempurature"
MELTING_POINT = "melting_point"
DUCTILITY = "ductility"
ADD_ACTIVITY = "add_activity"
BEAUTY = "beauty"
HARDNESS = "hardness"
DENSITY = "density"
DESCRIPTION = "description"

MINE_FUNCTION = "./src/database/mine_function.csv"
MIN_TEMPURATURE = "min_tempurature"
MAX_TEMPURATURE = "max_tempurature"
LEVEL_VART = "level_vary"

MAX_TEM = 2000

class Stone(object):
    '''石头抽象类'''
    def __init__(self, name:str, level=0):
        self.name = name
        self.level = level
        super(Stone, self).__init__()
        self._update()
    
    def _update(self):
        self.priority = None
        self.add_tempurature = None
        self.melting_point = None
        self.add_activity = None
        self.ductility = None
        self.beauty = None
        self.hardness = None
        self.density = None
        self.description = None
        
        mine_table = pd.read_csv(STONE_TABLE, encoding="gb2312")
        condition = (
            (mine_table['name'] == self.name) |
            (mine_table['english_name'] == self.name)
        )
        # 获取符合条件的行
        result = mine_table[condition]
        print("result", result)
        if not result.empty:
            self.priority = int(result.iloc[0][PRIORITY]) + self.level
            self.add_tempurature = int(result.iloc[0][ADD_TEMPURATURE])
            self.melting_point = int(result.iloc[0][MELTING_POINT])
            self.add_activity = int(result.iloc[0][ADD_ACTIVITY])
            self.ductility = int(result.iloc[0][DUCTILITY]) + self.level
            self.beauty = int(result.iloc[0][BEAUTY]) + self.level
            self.hardness = int(result.iloc[0][HARDNESS]) + self.level
            self.density = float(result.iloc[0][DENSITY])
            self.description = str(result.iloc[0][DESCRIPTION])
    
    def getDetail(self):
        msg = ""
        msg += f"{self.name}"
        if self.level > 0:
            msg += "+"
            msg += f"{self.level}"
        msg += f"\r\n{self.description}"
        msg += f"\r\n美观度：{self.beautyImform(self.beauty)}"
        msg += f"\r\n延展性：{self.ductilityImform(self.ductility)}"
        msg += f"\r\n硬度：{self.hardnessImform(self.hardness)}"
        msg += f"\r\n密度：{self.densityImform(self.density)}"
        return msg
    
    @classmethod
    def exist(self, name):
        mine_table = pd.read_csv(STONE_TABLE, encoding="gb2312")
        condition = (
            (mine_table['name'] == name) |
            (mine_table['english_name'] == name)
        )
        # 获取符合条件的行
        result = mine_table[condition]
        if not result.empty:
            return True
        else:
            return False

    @classmethod
    def ductilityImform(self, percentage):
        ranges = [
            (0, 10, "1级，一碰就碎，无法拉伸或塑形"),
            (10, 20, "2级，弯折就会崩断，仅能切割"),
            (20, 30, "3级，可承受小幅度弯曲，但反复弯折会断裂"),
            (30, 40, "4级，能被锤打成薄片，但边缘易开裂"),
            (40, 50, "5级，可拉伸成细丝，但长度有限"),
            (50, 60, "6级，能自由弯曲成复杂形状，不易断裂"),
            (60, 70, "7级，可拉伸至原长度的3倍以上，回弹力低"),
            (70, 80, "8级，像面团一样任意揉捏，几乎不会断裂"),
            (80, 90, "9级，流动感极强，需低温保存防止变形"),
            (90, 100, "10级，可像吹玻璃一样吹制成薄如蝉翼的形态，自动修复微裂纹"),
        ]
        
        for (low, high, text) in ranges:
            if low <= percentage <= high:
                return text
        return "未知"  # 默认情况（理论上不会执行）
    
    @classmethod
    def beautyImform(self, percentage):
        ranges = [
            (0, 10, "1级，表面坑洼不平，颜色浑浊如淤泥"),
            (10, 20, "2级，布满裂痕，像被酸液腐蚀过的废铁"),
            (20, 30, "3级，灰色质表面，无任何光泽或纹理，如同路边碎石"),
            (30, 40, "4级，在特定角度下反射弱光，像蒙尘的旧器"),
            (40, 50, "5级，表面细腻如陶土，颜色均匀但缺乏亮点"),
            (50, 60, "6级，像玉石般透亮，光线在内部柔和流动"),
            (60, 70, "7级，表面镶嵌细小晶体，如同繁星嵌入夜空"),
            (70, 80, "8级，随角度变化呈现彩虹色渐变，像极光被封印在石中"),
            (80, 90, "9级，散发柔和金芒，仿佛蕴含神性力量，驱散周围黑暗"),
            (90, 100, "10级，形态不断变幻，时而如银河漩涡，时而如天使羽翼，观测者会陷入痴迷"),
        ]
        
        for (low, high, text) in ranges:
            if low <= percentage <= high:
                return text
        return "未知"  # 默认情况（理论上不会执行）
    
    @classmethod
    def hardnessImform(self, percentage):
        ranges = [
            (0, 10, "1级，手指轻压即变形，甚至能被风吹散，接触空气会缓慢挥发"),
            (10, 20, "2级，用木棍轻敲即碎成粉末，无法承受自身重量"),
            (20, 30, "3级，可随意揉捏成形，但会融化，也会硬化开裂"),
            (30, 40, "4级，需金属工具切割，可缓冲冲击但易老化变脆"),
            (40, 50, "5级，需铁器才能刮花，可承受轻度撞击，但长期受力会断裂"),
            (50, 60, "6级，需专业工具才能切割，能反弹普通箭矢，但锤击会留下凹痕"),
            (60, 70, "7级，仅能被同级或更高硬度材料刮伤，天然抗磨损"),
            (70, 80, "8级，吸收动能并分散冲击，连爆炸都难以留下痕迹"),
            (80, 90, "9级，抗压缩能力强但脆性高，爆炸冲击下保持完整"),
            (90, 100, "10级，仅能被金刚石工具加工，自然磨损极慢，能承受高强度冲击"),
        ]
        
        for (low, high, text) in ranges:
            if low <= percentage <= high:
                return text
        return "未知"  # 默认情况（理论上不会执行）
    
    @classmethod
    def densityImform(self, percentage):
        ranges = [
            (0, 1, "单位体积质量极低，结构松散易压缩，可漂浮于液体表面"),
            (1, 2, "质量轻且孔隙较多，可浮于盐水表面"),
            (2, 3, "单位体积质量适中"),
            (3, 4, "单位体积质量较重，沉入水底且快速沉降"),
            (4, 5, "单位体积质量较高"),
            (5, 6, "单位体积质量高"),
            (6, 7, "单位体积质量非常高"),
            (7, 8, "单位体积质量接近岩石极限"),
            (8, 9, "沉入水底并破坏容器结构"),
            (9, 10, "矿石材料中密度最高"),
        ]
        
        for (low, high, text) in ranges:
            if low <= percentage <= high:
                return text
        return "未知"  # 默认情况（理论上不会执行）
    
class Mine(User):
    def __init__(self, user_id:int):
        super(Mine, self).__init__(user_id=user_id, database_path=DATABASE_PATH)
        self._update()

    def _update(self):
        super()._update()
        # 获取加工炉内的矿石及其状态
        
        # 初始矿石名称
        t = self.read(STONENAME)
        if t == None:
            self.stone_name = "无"
            self.write(STONENAME, self.stone_name)
        else:
            self.stone_name = str(t)
        
        # 矿石等级
        t = self.read(LEVEL)
        if t == None:
            self.level = 0
            self.write(LEVEL, self.level)
        else:
            self.level = int(t)
        
        # 加工炉温度
        t = self.read(TEMPURATURE)
        if t == None:
            self.tempurature = 27
            self.write(TEMPURATURE, self.tempurature)
        else:
            self.tempurature = int(t)

        # 锅炉反应活跃度
        t = self.read(ACTIVITY)
        if t == None:
            self.activity = 0
            self.write(ACTIVITY, self.activity)
        else:
            self.activity = int(t)
        
        # 仓库
        t = self.read(STORAGE)
        if t == None:
            self.storage = []
            self.write(STORAGE, self.list2Str(self.storage))
        else:
            self.storage = self.str2List(t)
    
    def look(self):
        '''获取炉内信息'''
        msg = ""
        
        msg += f"\r\n炉内矿石：{self.stone_name}"
        if self.level > 0:
            msg += f"+{self.level}"
        msg += f"\r\n炉内温度：{self.tempuratureImform(self.tempurature)}({self.tempurature}℃)"
        msg += f"\r\n反应活性：{self.activityImform(self.activity)}({self.activity}%)"
        # 还有其他信息吗？
        
        return msg
    
    def throw(self, stone_name:str, level=0):
        '''向加工炉内扔入矿物'''
        
        msg = ""
        
        if not Stone.exist(stone_name):
            msg += f"不存在该矿石[{stone_name}]"
            return msg
        
        stone_name_level = str(stone_name)
        if level > 0:
            stone_name_level = str(stone_name) + "+" + str(level)
        if not stone_name_level in self.storage and stone_name_level != "无":
            msg += f"你没有该矿石[{stone_name_level}]"
            return msg
        
        stone_old = Stone(name=self.stone_name, level=self.level)
        stone_new = Stone(stone_name, level=level)
        
        # 获得较高权重矿石的等级
        if stone_old.priority > stone_new.priority:
            high_priority_level = stone_old.level
        else :
            high_priority_level = stone_new.level
        
        # 查询合成表
        # 存在合成表，物品变化
        stone_combined_name_lv = self.searchMineFunction(self.tempurature, self.activity, stone_old.name, stone_new.name)
        if stone_combined_name_lv[0] != "none":
            stone_combined = Stone(name=stone_combined_name_lv[0])
            # 无特殊说明，权重上升，等级降1，权重不变，等级不变。
            if stone_combined_name_lv[1] == None:
                if stone_combined.priority > stone_old.priority and stone_combined.priority > stone_new.priority:
                    stone_combined.level = high_priority_level - 1
                else:
                    stone_combined.level = high_priority_level
            # 有说明，令等级上升或下降
            else:
                stone_combined.level = high_priority_level + stone_combined_name_lv[1]
            
            
            msg += f"\r\n合成了新矿物：{stone_combined.name}"
            if stone_combined.level < 0:
                stone_combined.level = 0
            if stone_combined.level > 10:
                stone_combined.level = 10
            if stone_combined.level > 0:
                msg += f"+{stone_combined.level}"
        
        # 无特殊合成表
        # 相同物品，在熔点大于矿物熔点时升级
        if stone_combined_name_lv[0] == "none":
            if stone_new.name == stone_old.name:
                stone_combined = Stone(name=stone_old.name, level=high_priority_level)
                if self.tempurature > stone_combined.melting_point:
                    stone_combined.level += 1
                    if stone_combined.level > 10:
                        stone_combined.level = 10
                    msg += f"\r\n矿物升级为：{stone_combined.name}"
                else:
                    msg += f"\r\n未产生新矿物，锅中矿物为：{stone_combined.name}"
                if stone_combined.level > 0:
                    msg += f"+{stone_combined.level}"
            # 不相同物品，产物为高优先级物品，相同优先级为旧物品
            else:
                if stone_new.priority > stone_old.priority:
                    stone_combined = stone_new
                else:
                    stone_combined = stone_old
                msg += f"\r\n未产生新矿物，锅中矿物为：{stone_combined.name}"
                if stone_combined.level > 0:
                    msg += f"+{stone_combined.level}"
        
        if stone_name_level in self.storage:
            self.storage.remove(stone_name_level)
        
        # 改变锅炉温度
        if stone_new.add_tempurature > 0:
            self.tempurature = self.tempurature + (2000-self.tempurature)*stone_new.add_tempurature/100
            msg += f"\r\n炉内温度升高了。({self.tempurature}℃)"
        if stone_new.add_tempurature < 0:
            self.tempurature = self.tempurature + (self.tempurature-27)*stone_new.add_tempurature/100
            msg += f"\r\n炉内温度降低了。({self.tempurature}℃)"
        
        # 改变反应活性
        self.activity += stone_new.add_activity
        if stone_new.add_activity < 0:
            msg += f"\r\n反应活性降低了。({self.activity}%)"
        if stone_new.add_activity > 0:
            msg += f"\r\n反应活性提高了。({self.activity}%)"
        
        if self.activity < 0:
            self.activity = 0
        
        # 存储新矿物
        self.write(STONENAME, stone_combined.name)
        self.write(LEVEL, stone_combined.level)
        self.write(TEMPURATURE, self.tempurature)
        self.write(ACTIVITY, self.activity)
        self.write(STORAGE, self.list2Str(self.storage))
        
        return msg
    
    def take(self):
        '''冷却后取出加工炉内的矿物'''
        msg = ""
        stone_name_level = str(self.stone_name)
        if self.stone_name == "无":
            msg += "炉内是空的。"
            return msg
        if self.level>0:
            stone_name_level = str(self.stone_name) + "+" + str(self.level)
        self.storage.append(stone_name_level)
        self.write(STORAGE, self.list2Str(self.storage))
        self.init()
        msg += f"\r\n已取出矿物[{stone_name_level}]"
        return msg
    
    def init(self):
        self.write(STONENAME, "无")
        self.write(LEVEL, "0")
        self.write(TEMPURATURE, 27)
        self.write(ACTIVITY, 0)
    
    def mystone(self):
        msg = "\r\n你存储的矿石如下："
        
        if self.storage == []:
            msg += "\r\n空空如也！"
            return msg
        
        count_dict = {}
        for item in self.storage:
            count_dict[item] = count_dict.get(item, 0) + 1
        
        # count_dict = {"燃料":1,"水晶":7}
        
        i = 0
        for item, count in count_dict.items():
            msg += f"{item}x{count}。"
            i += 1
            if i >=10:
                i = 0
                msg += "\r\n"
        
        return msg
    
    def give(self, name, num:int=1, level=0):
        msg = ""
        if not Stone.exist(name):
            msg += f"不存在该物品{name}"
            return msg
        # for i in range(int(num)):
        self.storage.append(name)
        msg += f"已获得{num}个{name}"
        self.write(STORAGE, self.list2Str(self.storage))
        
        return msg
    
    @classmethod
    def searchMineFunction(self, tempurature, activity, stone1_name, stone2_name):
        '''搜索合成表'''
        function_table = pd.read_csv(MINE_FUNCTION, encoding="gb2312")
        
        # 筛选条件
        condition = (
            (function_table['min_tempurature'] <= tempurature) & 
            (function_table['max_tempurature'] >= tempurature) & 
            (function_table['min_activity'] <= activity) & 
            (function_table['max_activity'] >= activity) & 
            (
                ((function_table['mine1'] == stone1_name) & (function_table['mine2'] == stone2_name)) |
                ((function_table['mine2'] == stone1_name) & (function_table['mine1'] == stone2_name)) |
                ((function_table['mine1'] == "all") & (function_table['mine2'] == stone1_name)) |
                ((function_table['mine1'] == "all") & (function_table['mine2'] == stone2_name)) |
                ((function_table['mine2'] == "all") & (function_table['mine1'] == stone1_name)) |
                ((function_table['mine2'] == "all") & (function_table['mine1'] == stone2_name)) |
                ((function_table['mine1'] == "all") & (function_table['mine2'] == "all"))
            )
        )
        
        # 获取符合条件的行
        result = function_table[condition]
        
        if result.empty:
            return ["none", None]
        
        if str(result.iloc[0][LEVEL_VART]) == "nan":
            lv = None
        else:
            lv = int(result.iloc[0][LEVEL_VART])
        
        stone_name_levelvary = [result.iloc[0]["name"], lv]
        return stone_name_levelvary
    
    @classmethod
    def tempuratureImform(self, tempurature):
        ranges = [
            (-273, -250, "-5级，分子都要被冻结了"),
            (-250, -100, "-4级，非常冷"),
            (-100, 0, "-3级，小于冰点"),
            (0, 10, "-2级，快要结冰了"),
            (10, 20, "-1级，有点凉"),
            (20, 40, "0级，常温"),
            (40, 100, "1级，有点热"),
            (100, 500, "2级，充满了水汽"),
            (500, 1000, "3级，适合熔炼大部分矿物"),
            (1000, 1500, "4级，对于大部分矿物来说，温度稍微有点高"),
            (1500, 1900, "5级，温度有点高过头了"),
            (1900, 2000, "6级，温度已在可达上限附近"),
        ]
        
        for (low, high, text) in ranges:
            if low <= tempurature <= high:
                return text
        return "未知"  # 默认情况（理论上不会执行）
    
    @classmethod
    def activityImform(self, activity):
        ranges = [
            (0, 10, "1级，极低，几乎不参与反应，化学性质极其稳定。"),
            (10, 20, "2级，低，反应速率缓慢。"),
            (20, 30, "3级，较低，特定条件下可反应，但效率较低"),
            (30, 40, "4级，中等偏下，常温下反应缓慢，加热可加速。"),
            (40, 50, "5级，中等，常规条件下可反应，需一定时间。"),
            (50, 60, "6级，中等偏上，反应速率较快，短时间内可见变化。"),
            (60, 70, "7级，较高，易反应，需控制条件避免副反应。"),
            (70, 80, "8级，高，剧烈反应，需严格安全措施。"),
            (80, 90, "9级，极高，瞬间反应，存在爆炸风险。"),
            (90, 100, "10级，极端，极不稳定，即将发生剧烈反应。"),
            (100, 10000, "锅炉已经爆炸了"),
        ]
        
        for (low, high, text) in ranges:
            if low <= activity <= high:
                return text
        return "未知范围"  # 默认情况（理论上不会执行）
    
    # 以下是辅助函数
    def str2List(self, s:str) -> list[str, int]:
        '''将字符串 s="none|none|none+3|水晶+3" 变为列表 l=["none", "none", "none+3", "水晶+3"] '''
        if not s:
            return dict()
        
        str_list = s.split("|") # ["a:123", "b:456"]
        return str_list
    
    def list2Str(self, l:list) -> str:
        '''将列表 l=["none", "none", "none+3", "水晶+3"]变为 字符串 s="none|none|none+3|水晶+3" '''
        s = "|".join(l)
        return s



