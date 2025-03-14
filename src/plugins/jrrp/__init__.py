from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent
# from nonebot.adapters.onebot.v11 import GroupMessageEvent
# from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.plugin import PluginMetadata
import random as rd
import time as tm
from user.jrrpState import jrrpState
from user.pet import Pet

__plugin_meta__ = PluginMetadata(
    name="jrrp",
    description="今日人品",
    usage="/jrrp",
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


# 0、从群里读出jrrp指令
jrrp = on_command("jrrp")

@jrrp.handle()
async def handle_jrrp(event: MessageEvent):
    
    # 1、获取用户账号
    id = event.user_id
    state = jrrpState(id)
    p = Pet(id)
    
    # 1.1、检测是否进行过jrrp，如是，则输出jrrp值
    if(state.jrrped()):
        msg = "你已经jrrp过了，你的jrrp值为：" + str(state.value) + "。" + state.get_jrrp_text()
        await jrrp.finish(message=msg)
    
    # 2、获取当前时间
    time = tm.time_ns()
    
    # 2.1、设置下次jrrp至少要等待到的时间(下一个22点)
    state.set_next_time()
    
    # 3、根据账号和时间设置一个随机数种子，并依此产生随机数
    randint = get_a_random_number(id, time)
    
    # 4、转化随机数为输出
    state.set_jrrp(randint)
    msg="你的jrrp值为：" + str(randint) + "。" + state.get_jrrp_text()
    msg += "\r\n" + p.addExpbyJRRP(randint)
    await jrrp.finish(message=msg, at_sender = True)


