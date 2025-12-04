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

TIME_NAN = "2000-01-01 00:00:00"

# 0、从群里读出jrrp指令
music = on_command("music")
guess = on_command("guess")
giveup = on_command("giveup")

# TEMP_PATH = "./src/database/music/1/ST1.mp4"
# TEMP_PATH = "./src/database/music/1/城市之上.mp4"
# TEMP_PATH = "./src/database/music/1/坠落谜题.mp4"
# TEMP_PATH = "./src/database/music/1/玫瑰花园.mp4"

index_now = 0
guess_state = False
total_ans = 0
begin_time = datetime.now() - dt.timedelta(seconds=30)

CRY_AWARD = 3

def isXsLastTime(last_time: datetime, scnds):
    current_time = datetime.now()
    if current_time - last_time > dt.timedelta(seconds=scnds):
        return True
    return False

@music.handle()
async def handle_music(event: GroupMessageEvent, arg: Message = CommandArg()):
    global guess_state
    global index_now
    global total_ans
    global begin_time
    total_ans = 0
    if guess_state:
        await music.finish()
    
    if not isXsLastTime(begin_time, scnds=15):
        await music.finish()
    
    args = str(arg).lower().split()
    
    if len(args) != 1 and len(args) != 0:
        await music.finish()
    
    index_now = RandomVideo.getRandomIndex()
    # index_now = 100
    
    # 控制难度
    rd.seed(tm.time_ns())
    rand_time = rd.randint(1, 10)
    
    all_music = False
    if len(args) != 0:
        if str(arg[0]) == "e":
            rand_time = 10
        if str(arg[0]) == "n":
            rand_time = 5
        if str(arg[0]) == "h":
            rand_time = 2
        if str(arg[0]) == "l":
            rand_time = 1
        if str(arg[0]) == "all":
            all_music = True
            rand_time = -1
        elif float(str(arg[0]))>0 and float(str(arg[0]))<10:
            rand_time = float(str(arg[0]))
    
    output_music_path = RandomVideo.getRandomClip(song_index=index_now, clip_duration=rand_time)
    if not os.path.exists(output_music_path):
        msg = f"ValueError: there is no file in {output_music_path}"
        await music.finish(message=msg)
    # ValueError: cannot convert float NaN to integer
    
    output_music_path = "file:///" + os.path.abspath(output_music_path)
    
    msg = MessageSegment.record(file=output_music_path)
    
    guess_state = True
    if all_music:
        guess_state = False
        await music.send(message=f"接下来播放{RandomVideo.getName(index_now)}")
    begin_time = dt.datetime.now()
    await music.finish(message=msg)

@guess.handle()
async def handle_guess(event: GroupMessageEvent, arg: Message = CommandArg()):
    global guess_state
    global index_now
    global total_ans
    if not guess_state:
        await music.finish()
    
    args = str(arg).lower().split()
    
    if len(args) != 1:
        await guess.finish()
    
    name = str(args[0])
    
    print(f"name: {name}")
    print(f"RandomVideo.getName(index_now): {RandomVideo.getName(index_now)}")
    
    if name in RandomVideo.getAlias(index_now):
        user_id = event.user_id
        p = Pet(user_id=user_id)
        
        guess_state = False
        msg = f"正确，答案是{RandomVideo.getName(index_now)}"
        msg += p.addCry(CRY_AWARD)
        await guess.finish(message=msg, at_sender=True)
    else:
        total_ans+=1
        if total_ans > 5:
            msg= "你们的猜测是错误的！"
            total_ans = 0
            await guess.send(message=msg)
        await guess.finish()

@giveup.handle()
async def handle_giveup(event: GroupMessageEvent):
    global guess_state
    
    if not guess_state:
        await giveup.finish()
        
    guess_state = False
    msg = f"已放弃。答案是{RandomVideo.getName(index_now)}"
    await giveup.finish(message=msg)
