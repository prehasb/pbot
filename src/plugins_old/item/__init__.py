from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment
# from nonebot.adapters.onebot.v11 import GroupMessageEvent
# from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.plugin import PluginMetadata
import random as rd
from nonebot.permission import SUPERUSER

from user.item.itemOperation import ItemOperation

from nonebot.adapters import Message
from nonebot.params import CommandArg

__plugin_meta__ = PluginMetadata(
    name="item",
    description="道具",
    usage="",
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


buy = on_command("buy")    

@buy.handle()
async def handle_buy(event: MessageEvent, arg: Message = CommandArg()):
    args = str(arg).lower().split()
    
    if len(args) !=1 and len(args) != 2:
        await buy.finish()
    
    if len(args) == 1:
        number = 1
    elif len(args) == 2:
        number = int(args[1])
    
    # 0、获取用户id
    user_id = event.user_id
    item_name = args[0]
    io = ItemOperation(user_id=user_id)
    msg = io.buy(item_name, number)
    
    if msg == "":
        await buy.finish()
    
    await buy.finish(message=msg, at_sender = True)

use = on_command("use")

@use.handle()
async def handle_use(event: MessageEvent, arg: Message = CommandArg()):
    args = str(arg).lower().split()
    
    if len(args) !=1 and len(args) != 2:
        await use.finish()
    
    if len(args) == 1:
        number = 1
    elif len(args) == 2:
        number = int(args[1])
    
    item_name = args[0]
    print("item_name: ", item_name)
    
    # 0、获取用户id
    user_id = event.user_id
    
    io = ItemOperation(user_id=user_id)
    msg = io.use(item_name, number)
    
    if msg == "":
        await buy.finish()
    
    await use.finish(message=msg, at_sender = True)

item = on_command("item")

@item.handle()
async def handle_item(event: MessageEvent, arg: Message = CommandArg()):
    args = str(arg).lower().split()
    
    if len(args) !=1:
        await item.finish()
    
    # 0、获取用户id
    user_id = event.user_id
    item_name = args[0]
    io = ItemOperation(user_id=user_id)
    msg = io.describe(item_name)
    
    await item.finish(message=msg, at_sender = True)

shop = on_command("shop")
@shop.handle()
async def handle_shop(event: MessageEvent):
    msg = ItemOperation.shop()
    await shop.finish(message=msg)
    
myitem = on_command("myitem")
@myitem.handle()
async def handle_shop(event: MessageEvent):
    user_id = event.user_id
    io = ItemOperation(user_id=user_id)
    
    msg = io.myitem()
    
    await myitem.finish(message=msg, at_sender = True)

