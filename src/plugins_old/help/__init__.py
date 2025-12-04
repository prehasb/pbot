from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent
# from nonebot.adapters.onebot.v11 import GroupMessageEvent
# from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.plugin import PluginMetadata
import random as rd
import time as tm
from user.jrrpState import jrrpState

__plugin_meta__ = PluginMetadata(
    name="help",
    description="今日人品",
    usage="/help",
    type="application",
    config=None,
    supported_adapters=None,
)

# 0、从群里读出jrrp指令
help = on_command("help")

'''
'''

HELP_TEXT = '''    - 想领养一只电子玛德琳宠物吗？本波特将实现你的这一愿望。
    - 每个玛德琳都有自己的等级，通过自然产生或工厂自动加工的经验来升级你的玛德琳吧
    - 指令：
    - ck: 查看你的玛德琳经验值和名称以及状态。初次使用该指令领取新的玛德琳
    - takeall: 拿走存储的经验和水晶
    - build: 消耗水晶升级工厂，增加获取经验和水晶的速度
    - jrrp: 查看今日人品，根据今日人品值随机增加经验值
    - music: 随机生成一段草莓酱音乐，输入guess猜测，输入giveup放弃
    - feed <num>: 给你的玛德琳喂养水晶以让其升级
    - shop: 查看商店的物品与价格
    - item <name>: 查询<name>道具的功能
    - buy <name>: 购买<name>道具
    - use <name>: 使用<name>道具
    - letter: 收取玛德琳寄给你的信件'''
    # - rate: 查看当前汇率
    # - changes <num>: 花费水晶，获得<num>个草莓(S trawberry)
    # - changec <num>: 花费草莓，获得<num>个水晶(C rystal)'''
    
'''
'''

@help.handle()
async def handle_jrrp(event: MessageEvent):
    msg = HELP_TEXT
    await help.finish(message=HELP_TEXT)


