from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent
# from nonebot.adapters.onebot.v11 import GroupMessageEvent
# from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.plugin import PluginMetadata
import random as rd
import time as tm
from user.jrrpState import jrrpState
from nonebot.permission import SUPERUSER

__plugin_meta__ = PluginMetadata(
    name="help",
    description="今日人品",
    usage="/help",
    type="application",
    config=None,
    supported_adapters=None,
)

# 0、从群里读出jrrp指令
bet4 = on_command("bet4", permission=SUPERUSER)

'''
'''

HELP_TEXT = '''    - 想领养一只电子玛德琳宠物吗？本波特将实现你的这一愿望。
    - 每个玛德琳都有自己的等级，通过自然产生或工厂自动加工的经验来升级你的玛德琳吧
    - 指令：
    - ck: 查看你的玛德琳经验值和名称以及状态。初次使用该指令领取新的玛德琳
    - takeall: 拿走存储的所有经验值
    - build: 消耗冲刺水晶升级一次工厂，增加获取经验和水晶的速度
    - jrrp: 查看今日人品，根据今日人品值随机增加经验值
    - feed <num>: 给你的玛德琳喂养水晶以让其升级
    - music: 随机生成一段草莓酱音乐，输入guess猜测，输入giveup放弃
    - shop: 查看商店的物品与价格
    - item <name>: 查询<name>道具的功能
    - buy <name>: 购买<name>道具
    - use <name>: 使用<name>道具(若道具可使用)'''
    
'''
'''

@bet4.handle()
async def handle_bet4(event: MessageEvent):
    rd.seed()
    int1 = rd.randint(1,10)
    int2 = rd.randint(1,10)
    int3 = rd.randint(1,10)
    msg = ".bank take 300"
    await bet4.send(message=msg)
    msg = f".bet4/{int1}/{int2}/{int3}"
    await bet4.send(message=msg)
    msg = f".bet4/{rd.randint(1,10)}/{rd.randint(1,10)}/{rd.randint(1,10)}"
    await bet4.finish(message=msg)


