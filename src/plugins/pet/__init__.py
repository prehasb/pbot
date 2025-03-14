from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment
# from nonebot.adapters.onebot.v11 import GroupMessageEvent
# from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.plugin import PluginMetadata
import random as rd
import time as tm
from user.pet import Pet
import pandas as pd
from nonebot.permission import SUPERUSER

from nonebot.adapters import Message
from nonebot.params import CommandArg

__plugin_meta__ = PluginMetadata(
    name="pet",
    description="玛德琳:宠物",
    usage="/pet",
    type="application",
    config=None,
    supported_adapters=None,
)

THRESHOLD_HOUR = 22
THRESHOLD_MINUTE = 0

TIME_NAN = "2000-01-01 00:00:00"

def get_a_random_number(userid: int, time: int) -> int:
    '''根据用户id和当前时间生成随机数'''
    rd.seed(userid + time)
    rslt = rd.randint(0, 100)
    return rslt


# 0、从群里读出ck指令
ck = on_command("ck")

@ck.handle()
async def handle_jrrp(event: MessageEvent):
    # 0、获取用户id
    user_id = event.user_id
    
    # 1、根据当前时间差获取玛德琳等级和水晶
    p = Pet(user_id)
    exp_num = p.getExpNum()
    cry_num = p.getCryNum()
    # at_segment = MessageSegment.at(user_id)
    
    msg = ""
    msg += f"\r\n- 待领取: {exp_num}/{p.getMaxSaveExp()}经验值，{cry_num}冲刺水晶"
    msg += f"\r\n- 当前玛德琳: lv{p.level} {p.getName()}"
    if p.getImagePath() != None:
        msg += MessageSegment.image(file=p.getImagePath())
    msg += f"\r\n- 当前经验值: {p.exp}/{p.getLevelUpExp()}，当前冲刺水晶: {p.crystal_num}个"
    if p.getLevelUpCry() > 0:
        msg += f"\r\n- 你的玛德琳想吃{p.feeded_cry}/{p.getLevelUpCry()}个水晶。"
    msg += f"\r\n- 工厂等级为: {p.getFacName()}，升级所需水晶数量为{p.getFacLevelupCry()}"
    msg += f"\r\n- 工厂每秒加工{p._getFacrotyExpPs()}点经验值，每小时生产{p._getFacrotyCryPh()}个冲刺水晶"
    
    await ck.finish(message=msg, at_sender=True)


takeall = on_command("takeall")

@takeall.handle()
async def handle_takeall(event: MessageEvent):
    # 0、获取用户id
    user_id = event.user_id
    
    # 1、根据当前时间差获取玛德琳等级和水晶
    p = Pet(user_id)
    exp_num = p.getExpNum()
    msg = MessageSegment.text("at")
    msg = f"你获得了{exp_num}经验值"
    cry_num = p.getCryNum()
    if cry_num != 0:
        msg += f"\r\n你获得了{cry_num}个冲刺水晶"
    
    # 2、如果玛德琳可以升级，则升级一次玛德琳，并将经验叠加到下一个等级
    msg += p.updateExpandCry()
    
    # 3、显示升级信息
    await takeall.finish(message=msg, at_sender = True)


build = on_command("build")

@build.handle()
async def handle_build(event: MessageEvent):
    # 0、获取用户id
    user_id = event.user_id
    
    p = Pet(user_id)
    
    msg = p.levelupFac()
    
    await build.finish(message=msg, at_sender = True)
    

feed = on_command("feed")    

@feed.handle()
async def handle_feed(event: MessageEvent, arg: Message = CommandArg()):
    args = str(arg).lower().split()
    
    if len(args) != 1:
        await feed.finish()
    
    feed_cry_num = int(args[0])
    
    # 0、获取用户id
    user_id = event.user_id
    p = Pet(user_id)
    
    # 1、喂养宠物个数水晶
    msg = p.feed(feed_cry_num)
    
    # 2、将返回的消息传给用户
    
    if msg == "":
        await feed.finish()
    
    await feed.finish(message=msg, at_sender = True)
    
giveall = on_command("全服发放", permission=SUPERUSER)

@giveall.handle()
async def handle_feed(event: MessageEvent, arg: Message = CommandArg()):
    args = str(arg).lower().split()
    
    if len(args) != 1:
        await feed.finish()
    
    give_cry_num = int(args[0])
    
    DATABASE_PATH = "./src/database/database.csv"
    db = pd.read_csv(DATABASE_PATH)
    max_row = db.shape[0]
    for row in range(0, max_row):
        db.at[row, "crystal_num"] += give_cry_num
    db.to_csv(DATABASE_PATH, index=False)
    await giveall.finish(message=f"已分发{give_cry_num}水晶")
    

