# '''
# Author: 萌新源
# Date: 2024-08-07 18:14:19
# LastEditTime: 2024-08-08 23:15:31
# LastEditors: 萌新源
# Description: 测试bot是否正常启动
# 个性签名：敲代码就仨字，我乐意
# '''
# from nonebot import on_regex
# from nonebot.typing import T_State
# from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message

# Test = on_regex(pattern=r'^测试$',priority=1)


# @Test.handle()
# async def Test_send(bot: Bot, event: GroupMessageEvent, state: T_State):
#     msg = "Bot启动正常"
#     await Test.finish(message=Message(msg))
