from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.plugin import PluginMetadata
import random as rd
import datetime as dt
import pandas as pd
from nonebot.permission import SUPERUSER
import requests
import json
from nonebot.adapters import Message
from nonebot.params import CommandArg
import nonebot
from nonebot import get_bot
from change.change import Change
from change.changeAPI import ChangeAPI
from user.pet import Pet

from .config import API_GROUP_ID
from .config import prehasb_id

__plugin_meta__ = PluginMetadata(
    name="change",
    description="汇率",
    usage="",
    type="application",
    config=None,
    supported_adapters=None,
)

ud = dict() # {用户id1: 群id1, 用户id2: 群id2}
user_cry = dict() # {用户id: 水晶数量}

testc = on_command("ttc")
@testc.handle()
async def handle_function(event: MessageEvent, message: Message = CommandArg()):
    bot = nonebot.get_bot()
    if any((not seg.is_text()) or str(seg) for seg in message):
        if event.user_id == prehasb_id:
            msg = str(message)
            print("msg: ", msg)
            await bot.send_group_msg(message = msg, group_id = API_GROUP_ID)
            await testc.send(message=msg)
        else:
            msg = "\0" +str(message)
            await bot.send_group_msg(message = msg, group_id = API_GROUP_ID)
            await testc.send(message=msg)
    testc.finish(message=msg)

rate = on_command("rate")
@rate.handle()
async def handle_rate(event: MessageEvent):
    msg = Change.rate_text()
    await rate.finish(message=msg)
    

buys = on_command("changes")
@buys.handle()
async def handle_function(event: GroupMessageEvent|PrivateMessageEvent, arg: Message = CommandArg()):
    bot = get_bot()
    args = str(arg).lower().split()
    user_id = event.user_id
    chg = Change(user_id)
    # 异常处理
    if len(args) != 1 or not args[0].isdecimal():
        await buys.finish()
    elif int(args[0])<=0:
        await buys.finish()
    
    # 正常逻辑 buys 100
    stb = int(args[0])
    msg = chg.askForBuyStrawberry(stb)
    
    # 水晶不足或银行存款不足，不OK
    if not chg.askForBuyStrawberryOK(stb):
        await buys.finish(message=msg, at_sender = True)
    
    # OK
    user_cry[user_id] = -chg.getCryNeededFor(stb)
    command_text = chg.sendBerryChangeText(stb)
    await bot.send_group_msg(message = command_text, group_id = API_GROUP_ID)
    if hasattr(event, 'group_id'):
        ud[event.user_id] = event.group_id
        print("event.group_id:", event.group_id)
    await buys.finish(message=msg, at_sender = True)

buyc = on_command("changec")
@buyc.handle()
async def handle_function(event: MessageEvent, arg: Message = CommandArg()):
    bot = get_bot()
    args = str(arg).lower().split()
    user_id = event.user_id
    chg = Change(user_id)
    # 异常处理
    if len(args) != 1 or not args[0].isdecimal():
        await buyc.finish()
    elif int(args[0])<=0:
        await buyc.finish()
    
    # 正常逻辑 buyc 100
    cry = int(args[0])
    msg = chg.askForBuyCrystal(cry)
    
    # 银行存款不足，不OK
    if not chg.askForBuyCrystalOK(cry):
        await buys.finish(message=msg, at_sender = True)
    
    # OK
    stb_needed = chg.getStbNeededFor(cry)
    user_cry[user_id] = cry
    command_text = chg.sendBerryCheckText(stb_needed)
    await bot.send_group_msg(message = command_text, group_id = API_GROUP_ID)
    if hasattr(event, 'group_id'):
        ud[event.user_id] = event.group_id
        print("event.group_id:", event.group_id)
    await buyc.finish(message=msg, at_sender = True)

@Change.check.handle()
async def handle_check(event: GroupMessageEvent, arg: Message = CommandArg()):
    # 获取数据
    bot = get_bot()
    args = str(arg).lower().split()
    user_id = int(args[0])
    threshold = int(args[1])
    status = int(args[2])
    chg = Change(user_id)
    # 处理收到的消息
    msg = chg.processBerryCheck(threshold, status)
    # 失败处理
    if status != 200:
        if user_id in ud:
            group_id = ud[user_id]
            del ud[user_id]
            del user_cry[user_id]
            await bot.send_group_msg(message = msg, group_id = group_id, at_sender = True)
        else:
            await bot.send_msg(message = msg, user_id = user_id)
        await Change.change.finish()
    
    # 成功处理
    command_text = chg.sendBerryChangeText(-threshold)
    await bot.send_group_msg(message = command_text, group_id = API_GROUP_ID)
    await Change.change.finish()

@Change.change.handle()
async def handle_change(event: GroupMessageEvent, arg: Message = CommandArg()):
    # 获取数据
    bot = get_bot()
    args = str(arg).lower().split()
    user_id = int(args[0])
    number = int(args[1])
    status = int(args[2])
    chg = Change(user_id)
    # 处理收到的消息
    msg = chg.processBerryChange(number, user_cry[user_id], status)
    del user_cry[user_id]
    # 完成处理
    if user_id in ud:
        group_id = ud[user_id]
        del ud[user_id]
        await bot.send_group_msg(message = msg, group_id = group_id, at_sender = True)
    else:
        await bot.send_msg(message = msg, user_id = user_id)
    await Change.change.finish()
