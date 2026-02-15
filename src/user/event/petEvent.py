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
TIME_DELAY = "next_time"
IS_FIRST_EVENT = "is_first_event"
NEXT_EVENT = "next_event"
CHOOSE = "choose"
ITEM = "item"
IMAGENAME = "imagename"
RANDOMIMAGE = "randomimage"

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
        time_delay = self.getTimeDelayById(self.last_event_id)
        if time_delay == 0:
            time_delay = NT_int
        last_time = self.next_event_time - dt.timedelta(minutes=time_delay)
        msg += str(last_time)
        return msg
    
    def activate(self) -> str:
        '''激活事件'''
        msg = ""
        
        self.event_id = self.pickNextEvent()
        
        if self.event_id == 0:
            self.event_id = self.pickRandomEvent()
        
        print("self.event_id: ", self.event_id)
        
        
        from item.darkmoonRuins.theDreamer import theDreamer
        td = theDreamer(self.user_id)
        
        if td.hasCD:
            msg += "\r\n你收到了来自旅行中的玛德琳的一封信："
        else:
            msg += "\r\n你自梦中收到一封信："
        
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
        
        if d:
            for name_in_useritem in d.keys():
                if d[name_in_useritem] != 0:
                    num = d[name_in_useritem]
                    name = ItemOperation.getNamebyNameInUseritem(name_in_useritem)
                    io = ItemOperation(user_id=self.user_id)
                    msg += io.give(name, num)
        
        self.write(LAST_EVENT_ID, self.event_id)
        
        NO_TIME_LIMIT_ID = [3520767439, 1]
        
        if (self.user_id not in NO_TIME_LIMIT_ID) and (td.hasCD):
            self.setNextTime()
        
        return msg
    
    def getImagePATH(self) -> str:
        name = self.readEventTable(IMAGENAME)
        random = self.readEventTable(RANDOMIMAGE)
        
        if name == 0:
            name = str(self.event_id)
        image_path = os.path.abspath(IMAGE_PATH) +"\\" + name
        if random == 0:
            image_path = image_path + ".png"
            if not os.path.exists(image_path):
                return None
        
        if random != 0:
            dp = DrawPhoto(image_path)
            dp.makeFinalPhoto()
            image_path = dp.outputTotalPhoto()
        
        file_image_path = "file:///" + image_path
        print("file_image_path: ", file_image_path)
        return file_image_path
    
    def setNextTime(self, hard_set_delay:int = None) -> str:
        time_delay = hard_set_delay
        if hard_set_delay == None:
            time_delay = self.getTimeDelay(hard_set_delay)
        next_time = datetime.now().replace(microsecond=0) + dt.timedelta(minutes=time_delay)
        self.next_event_time = next_time
        self.write(NEXT_EVENT_TIME, next_time)
    
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
        
    def getTimeDelayById(self, id, hard_set_delay = None) -> int:
        '''获取延迟的时间。若存在硬性时间(!=0)，则无视任何道具设置为硬性时间'''
        if hard_set_delay != None:
            return hard_set_delay
        
        time_delay = int(self.readEventTablebyID(id, TIME_DELAY))
        
        if time_delay == 0:
            time_delay = NT_int
        
        # 20250422添加：电子邮件，缩短等待时间
        #######################################################
        from item.email import email
        e = email(self.user_id)
        if e.number:
            time_delay -= e.skip_minute
        #######################################################
        
        return time_delay
    
    def getTimeDelay(self, hard_set_delay = None) -> int:
        '''获取延迟的时间。若存在硬性时间(!=0)，则无视任何道具设置为硬性时间'''
        return self.getTimeDelayById(self.event_id, hard_set_delay)
    
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
        item_str:str = self.readEventTable(ITEM)
        if item_str == 0:
            return dict()
        item_str_list = item_str.split("|") # ["test_item:5", "expSaveBall:2"]
        item_dict = dict() 
        
        for i in item_str_list:
            parts = i.split(':') # parts = ["test_item","5"]
            if len(parts) == 2:
                item_dict[parts[0]] = int(parts[1])
        return item_dict
    
    def getRandomImage(self) -> bool:
        '''查询是否随机生成图片'''
        ri = self.readEventTable(RANDOMIMAGE)
        if ri == 0:
            ri = False
        return bool(ri)
        
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
    
    def getNextEventDict(self) -> dict[int,int]:
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
        
        sum_p:int = 0
        for id in d.keys():
            sum_p += d[id] # sum_p = 5
        
        rd.seed()
        # sum_p 可能被d[id]强转换为浮点型
        random_number = rd.randint(1, int(sum_p)) # randint=2
        event_id = 0
        for id in d.keys():
            if random_number <= d[id]: # 1: randint = 2, 2:randing = 1
                event_id = id # 2 event_id = 5
                break
            random_number -= d[id] #1: randint = 1
        
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

from PIL import Image, ImageDraw

class DrawPhoto(object):
    
    final_photo = None
    width = 1600
    height = 1200
    scale_factor = 0.6
    max_iou = 0.001
    min_used_rate = 0.7
    
    def __init__(self, path:str):
        super(DrawPhoto, self).__init__()
        self.imagePath = path
        self.used_area = []
        self.file_list = []
        rd.seed()
        self.initImageFileList()
    
    def initImageFileList(self):
        # 列出文件夹中的所有文件
        files = os.listdir(self.imagePath)
        
        # 过滤出图片文件（根据常见的图片扩展名）
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        self.file_list = [file for file in files if file.lower().endswith(image_extensions)]
        print("self.file_list: ", self.file_list)
        if "bg.png" in self.file_list:
            self.file_list.remove("bg.png") # 过滤bg.png
        
    def outputTotalPhoto(self):
        if self.final_photo == None:
            self.final_photo = self.createNullImage()
        
        randnum = rd.randint(0, 1000)
        output_file = f"./cache/image{randnum}.png"
        self.final_photo.save(output_file, "PNG", quality=95)
        final_img_path = os.path.abspath(output_file)
        return final_img_path
    
    def makeFinalPhoto(self):
        repeat_num = 0
        while repeat_num < 100 and self.calculateUsedRate() < self.min_used_rate :
            if self.addRandomPhoto():
                repeat_num = 0
            else:
                repeat_num += 1
            
            if self.file_list == []:
                break
        
    def addRandomPhoto(self) -> bool:
        '''
        随机挑选照片窗口中的位置L(x, y)和一张图片I(img.size(width, height))
        
        若这个位置L可以放得下图片I，则放下图片并返回真，否则返回假
        
        :return: True: 位置L放得下图片I; Falst: 位置L放不下图片I
        '''
        image_name = self.getRandomImagePath()
        image_path = os.path.join(self.imagePath, image_name)
        if self.file_list == []:
            return False
        img = Image.open(image_path)
        # random_scale = rd.uniform(0.5, 0.7)
        # img = img.resize((int(img.size[0]*random_scale), int(img.size[1]*random_scale)))
        if img.size[0]/self.width > 0.2 or img.size[1]/self.height > 0.2:
            img = img.resize((int(img.size[0]*self.scale_factor), int(img.size[1]*self.scale_factor)))
        
        xy = self.getAUsablexy(img)
        if xy == None:
            xy = self.getRandomXY(img)
        
        xyxy = (xy, (xy[0]+img.size[0], xy[1]+img.size[1]))
        iou = self.calculateOverlap(xyxy)
        if iou > self.max_iou:
            return False
        
        self.file_list.remove(image_name)
        self.addNewPhoto(img, xy)
        self.used_area.append(xyxy)
        return True
    
    def getAUsablexy(self, img):
        min_x = 0
        min_y = 0
        max_x = self.width - img.size[0]
        max_y = self.height - img.size[1]
        # 均分num^2份宫格
        num = 9
        for i in range(num):
            for j in range(num):
                xy = (rd.randint(int(max_x*i/num), int(max_x*(i+1)/num)), rd.randint(int(max_y*j/num), int(max_y*(j+1)/num)))
                # print("xy: ", xy)
                xyxy = (xy, (xy[0]+img.size[0], xy[1]+img.size[1]))
                if self.isInside(xyxy) and self.calculateOverlap(xyxy) < self.max_iou:
                    return xy
        
        
        for used_photo in self.used_area:
            # 左侧
            x = used_photo[0][0] - img.size[0] + rd.randint(-10, 10)
            y = rd.randint(0, max_y)
            xy = (x, y)
            xyxy = (xy, (xy[0]+img.size[0], xy[1]+img.size[1]))
            if self.isInside(xyxy) and self.calculateOverlap(xyxy) < self.max_iou:
                return xy
            # 右侧
            x = used_photo[1][0] + rd.randint(-10, 10)
            y = rd.randint(0, max_y)
            xy = (x, y)
            xyxy = (xy, (xy[0]+img.size[0], xy[1]+img.size[1]))
            y = rd.randint(0, max_y)
            # 上侧
            x = rd.randint(0, max_x)
            y = used_photo[0][1] - img.size[1] + rd.randint(-10, 10)
            xy = (x, y)
            xyxy = (xy, (xy[0]+img.size[0], xy[1]+img.size[1]))
            if self.isInside(xyxy) and self.calculateOverlap(xyxy) < self.max_iou:
                return xy
            # 下侧
            x = rd.randint(0, max_x)
            y = used_photo[1][1] + rd.randint(-10, 10)
            xy = (x, y)
            xyxy = (xy, (xy[0]+img.size[0], xy[1]+img.size[1]))
            if self.isInside(xyxy) and self.calculateOverlap(xyxy) < self.max_iou:
                return xy
        return None
    
    def image2Photo(self, img, inner_border=20, outer_border=5, output_file = "./cache/image.png"):
        """
        为图片添加双层圆角边框
        :param img_path: 原始图片
        :return: 添加边框后的图片
        """
        # 计算总边框宽度
        total_border = inner_border + outer_border
        
        # 创建一个新的透明图层，比原图大总边框宽度
        bordered_img = Image.new("RGBA", 
                                (img.width + 2 * total_border, img.height + 2 * total_border),
                                (0, 0, 0, 0))
        
        # 创建外边框
        inner_mask = Image.new("RGBA", bordered_img.size, (0, 0, 0, 0))
        inner_draw = ImageDraw.Draw(inner_mask)
        
        # 绘制内边框的圆角矩形（白色）
        inner_rect = [
            (outer_border, outer_border),
            (bordered_img.width - outer_border, bordered_img.height - outer_border)
        ]
        inner_draw.rounded_rectangle(inner_rect, radius=int(inner_border*1.25), fill=(255, 255, 255, 255))
        
        # 创建外边框
        outer_mask = Image.new("RGBA", bordered_img.size, (0, 0, 0, 0))
        outer_draw = ImageDraw.Draw(outer_mask)
        
        # 绘制内边框的圆角矩形（灰色）
        outer_rect = [
            (0, 0),
            (bordered_img.width, bordered_img.height)
        ]
        outer_draw.rounded_rectangle(outer_rect, radius=int((outer_border+outer_border)*3), fill=(84, 84, 84, 255))
        # outer_draw.rounded_rectangle(outer_rect, radius=inner_border+outer_border, fill=(255, 255, 255))

        # 合并图像
        bordered_img.paste(outer_mask, (0, 0), outer_mask)
        bordered_img.paste(inner_mask, (0, 0), inner_mask)
        
        # 将原图粘贴到中心位置
        bordered_img.paste(img, (total_border, total_border))
        
        return bordered_img

    def createNullImage(self) -> Image:
        # 创建一个新的透明图层
        # 计算放大倍率
        
        bg = Image.open(self.imagePath + "\\bg.png")
        bg_x = bg.size[0]
        bg_y = bg.size[1]
        x_scale = self.width/bg_x
        y_scale = self.height/bg_y
        
        scale = max(x_scale, y_scale)
        
        bg = bg.resize((int(bg_x*scale), int(bg_y*scale)))
        null = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 160))
        bg.paste(null, (0, 0), null)
        bg = bg.crop((0,0,self.width,self.height))
        return bg
    
    def calculateUsedRate(self) -> float:
        used_area = 0
        for xy_used in self.used_area:
            x1 = xy_used[0][0]
            y1 = xy_used[0][1]
            x2 = xy_used[1][0]
            y2 = xy_used[1][1]
            used_area += (x2-x1) * (y2-y1)
        
        return used_area / (self.height*self.width)
    
    def calculateOverlap(self, xyxy) -> float:
        '''xyxy = ((x1, y1), (x2, y2))'''
        if self.used_area == []:
            return 0
        
        overlap_area = 0
        for xy_used in self.used_area:
            
            x1 = xy_used[0][0]
            y1 = xy_used[0][1]
            x2 = xy_used[1][0]
            y2 = xy_used[1][1]
            
            x3 = xyxy[0][0]
            y3 = xyxy[0][1]
            x4 = xyxy[1][0]
            y4 = xyxy[1][1]
            
            colInt = max(0, min(x2 ,x4) - max(x1, x3))
            rowInt = max(0, min(y2, y4) - max(y1, y3))
            overlap_area += colInt * rowInt
        
        return overlap_area / (self.height*self.width)
    
    def addNewPhoto(self, img:Image, xy) -> None:
        if self.final_photo == None:
            self.final_photo = self.createNullImage()
        
        photo = self.image2Photo(img)
        photo = photo.rotate(rd.randint(-10, 10) ,expand=True)
        
        self.final_photo.paste(photo, (xy[0]-50, xy[1]-50), photo)
    
    def getRandomImagePath(self) -> str:
        '''根据大小加权随机选择一个图片文件'''
        
        # 设置权重
        weights = []
        for img_name in self.file_list:
            with Image.open(os.path.join(self.imagePath, img_name)) as img:
                width, height = img.size # img.size:List[width, height]
                weights.append(width + height)
        
        # 调用choices函数，带权重选择
        random_image = rd.choices(self.file_list, weights=weights, k=1)[0]
        return random_image
    
    def getRandomXY(self, img:Image) -> tuple:
        max_x = 1600 - img.size[0]
        max_y = 1200 - img.size[1]
        x = rd.randint(0, max_x)
        y = rd.randint(0, max_y)
        return (x, y)
    
    def isInside(self, img:Image, xy:list) -> bool:
        min_x = 0
        min_y = 0
        max_x = self.width - img.size[0]
        max_y = self.height - img.size[1]
        if xy[0] < min_x or xy[0] > max_x or xy[1] < min_y or xy[1] > max_y:
            return False
        return True
    
    def isInside(self, xyxy) -> bool:
        if xyxy[0][0] < 0 or xyxy[1][0] > self.width or xyxy[0][1] < 0 or xyxy[1][1] > self.height:
            return False
        return True
        
        
    