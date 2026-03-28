from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11 import GroupMessageEvent
# from nonebot.adapters.onebot.v11 import PrivateMessageEvent
import random as rd
import time as tm
from datetime import datetime
import datetime as dt
from user.pet import Pet
import os
from video.video import RandomVideo
from nonebot.params import CommandArg
from Global import Global

TIME_NAN = "2000-01-01 00:00:00"

# 0、从群里读出jrrp指令
music = on_command("music")
guess = on_command("guess")
giveup = on_command("giveup")
set_default = on_command("sd")

# guess_state = False
# begin_time = datetime.now() - dt.timedelta(seconds=30)

INDEX_NOW = "index_now"
GUESS_STATE = "guess_state"
TOTAL_ANS = "total_ans"
BEGIN_TIME = "begin_time"

CRY_AWARD = 3

def isXsLastTime(last_time: datetime, scnds):
    current_time = datetime.now()
    if current_time - last_time > dt.timedelta(seconds=scnds):
        return True
    return False

@music.handle()
async def handle_music(event: GroupMessageEvent, arg: Message = CommandArg()):
    
    music_dict = Global(event.group_id).getMusicDict()
    
    # have begun
    if music_dict[GUESS_STATE]:
        await music.finish()
    
    # too fast
    if not isXsLastTime(music_dict[BEGIN_TIME], scnds=15):
        await music.finish()
    
    # too many input
    args = str(arg).lower().split()
    if len(args) != 1 and len(args) != 0:
        await music.finish()
        
    # init
    music_dict[TOTAL_ANS] = 0
    video = RandomVideo(music_dict)
    
    # difficulty
    rd.seed(tm.time_ns())
    rand_time = rd.randint(1, 10)
    
    def is_number(s):
        try:
            float(s)  # 尝试转换为 float（可以识别整数和小数）
            return True
        except ValueError:
            return False
    
    music_dict[INDEX_NOW] = video.getRandomIndex()
    all_music = False
    if len(args) != 0:
        if str(arg[0]) == "e":
            rand_time = 10
        elif str(arg[0]) == "n":
            rand_time = 5
        elif str(arg[0]) == "h":
            rand_time = 2
        elif str(arg[0]) == "l":
            rand_time = 1
        elif is_number(str(arg[0])) and float(str(arg[0]))>0 and float(str(arg[0]))<10:
            rand_time = float(str(arg[0]))
        elif str(arg[0]) != "all":
            all_music = True
            rand_time = -1
        elif video.getIndexByName(arg[0]):
            all_music = True
            rand_time = -1
            music_dict[INDEX_NOW] = video.getIndexByName(arg[0])
            
    output_music_path = video.getRandomClip(song_index=music_dict[INDEX_NOW], clip_duration=rand_time)
    if not os.path.exists(output_music_path):
        msg = f"ValueError: there is no file in {output_music_path}"
        await music.finish(message=msg)
    
    output_music_path = "file:///" + os.path.abspath(output_music_path)
    
    msg = MessageSegment.record(file=output_music_path)
    
    music_dict[GUESS_STATE] = True
    if all_music:
        music_dict[GUESS_STATE] = False
        await music.send(message=f"接下来播放{video.getName(music_dict[INDEX_NOW])}")
    music_dict[BEGIN_TIME] = dt.datetime.now()
    await music.finish(message=msg)

@guess.handle()
async def handle_guess(event: GroupMessageEvent, arg: Message = CommandArg()):
    
    music_dict = Global(event.group_id).getMusicDict()
    music_dict[TOTAL_ANS] = 0
    
    if not music_dict[GUESS_STATE]:
        await music.finish()
    
    args = str(arg).lower().split()
    
    if len(args) != 1:
        await guess.finish()
    
    name = str(args[0])
    
    print(f"name: {name}")
    print(f"RandomVideo.getName(music_dict[INDEX_NOW]): {RandomVideo.getName(music_dict[INDEX_NOW])}")
    
    if name in RandomVideo.getAlias(music_dict[INDEX_NOW]):
        user_id = event.user_id
        p = Pet(user_id=user_id)
        
        music_dict[GUESS_STATE] = False
        msg = f"正确，答案是{RandomVideo.getName(music_dict[INDEX_NOW])}"
        msg += p.addCry(CRY_AWARD)
        await guess.finish(message=msg, at_sender=True)
    else:
        music_dict[TOTAL_ANS]+=1
        if music_dict[TOTAL_ANS] > 5:
            msg= "你们的猜测是错误的！"
            music_dict[TOTAL_ANS] = 0
            await guess.send(message=msg)
        await guess.finish()

@giveup.handle()
async def handle_giveup(event: GroupMessageEvent):
    
    music_dict = Global(event.group_id).getMusicDict()
    if not music_dict[GUESS_STATE]:
        await giveup.finish()
        
    music_dict[GUESS_STATE] = False
    msg = f"已放弃。答案是{RandomVideo.getName(music_dict[INDEX_NOW])}"
    await giveup.finish(message=msg)
