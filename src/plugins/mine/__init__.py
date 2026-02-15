from nonebot import on_command
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER

import random as rd
import time as tm

from user.jrrpState import jrrpState
from user.pet import Pet
from user.factory.mine import Mine
from user.factory.mine import Stone

__plugin_meta__ = PluginMetadata(
    name="mine",
    description="矿石系统",
    usage="/mine",
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

stone = on_command("stone")

@stone.handle()
async def handle_throw(event: MessageEvent, arg: Message = CommandArg()):
    args = str(arg).lower().split()
    
    if len(args) !=1:
        await stone.finish()
    
    stome_name_level = str(args[0])
    
    l = stome_name_level.split("+")
    print("stome_name_level", l)
    stone_name = l[0]
    level = 0
    if len(l) == 2:
        level = int(l[1])
    
    sto = Stone(stone_name, level)
    
    msg = sto.getDetail()
    
    await stone.finish(message=msg)
    
mystone = on_command("mystone")

@mystone.handle()
async def handle_throw(event: MessageEvent):
    
    user_id = event.user_id
    mine = Mine(user_id=user_id)
    msg = mine.mystone()
    await mystone.finish(message=msg, at_sender=True)

look = on_command("look")

@look.handle()
async def handle_throw(event: MessageEvent):
    
    user_id = event.user_id
    mine = Mine(user_id=user_id)
    msg = mine.look()
    await look.finish(message=msg, at_sender=True)

fetch = on_command("fetch")

@fetch.handle()
async def handle_throw(event: MessageEvent):
    
    user_id = event.user_id
    mine = Mine(user_id=user_id)
    msg = mine.take()
    await fetch.finish(message=msg, at_sender=True)

throw = on_command("throw")

@throw.handle()
async def handle_throw(event: MessageEvent, arg: Message = CommandArg()):
    
    args = str(arg).lower().split()
    
    if len(args) !=1:
        await throw.finish()
    
    user_id = event.user_id
    stome_name_level = str(args[0])
    
    l = stome_name_level.split("+")
    print("stome_name_level", l)
    stome_name = l[0]
    level = 0
    if len(l) == 2:
        level = int(l[1])
    
    mine = Mine(user_id=user_id)
    
    msg = mine.throw(stome_name, level)
    
    await throw.finish(message=msg, at_sender=True)

givestone = on_command("givestone", permission=SUPERUSER)
@givestone.handle()
async def handle_givestone(event: MessageEvent, arg: Message = CommandArg()):
    
    args = str(arg).lower().split()
    
    if len(args) !=1 and len(args) !=2 and len(args) !=3:
        await throw.finish()
    
    name = ""
    num = 1
    level = 0
    
    if len(args) ==1:
        name = args[0]
    
    if len(args) ==2:
        num = args[1]
    
    if len(args) ==3:
        level = args[2]
        
    user_id = event.user_id
    
    stome_name = str(name) + "+" + str(level)
    level = 0
    
    mine = Mine(user_id=user_id)
    
    msg = mine.give(stome_name, num)
    
    await givestone.finish(message=msg, at_sender=True)

