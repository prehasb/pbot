from moviepy import ImageClip, AudioFileClip, VideoFileClip
import random as rd
from pydub import AudioSegment
import pandas as pd
import time as tm
import os

 
# 设置文件路径
IMAGE_PATH = './src/database/music/blank.png'  # 图片文件路径
audio_path = './src/database/music/2.mp4'  # MP3音频文件路径
output_path = './src/database/music/output.amr'  # 输出MP4文件路径

MUSIC_PATH = './src/database/music/music.csv'

FATHER_PATH = "./src/database/music/"

MAP_NAME = "map_name"
LOBBY = "lobby"

class RandomVideo(object):
    duration:int
    '''时间长度'''
    begin:int
    '''开始时间'''
    filepath:str
    '''文件位置'''
    
    def __init__(self, ):
        super(RandomVideo, self).__init__()
    
    @classmethod
    def getRandomIndex(self) -> int:
        database = pd.read_csv(MUSIC_PATH, encoding="gb2312") # get the database
        total_line = database.shape[0] # 获取总行数
        
        time = tm.time_ns()
        rd.seed(time)
        song_index = rd.randint(0,total_line-1) # pick a random song index
        return song_index
    
    @classmethod
    def getName(self, song_index:int) -> str:
        '''获取获取对应下标歌曲的alias列表List
        
        @param: song_index MUSIC_PATH的csv文件中的歌曲下标'''
        database = pd.read_csv(MUSIC_PATH, encoding="gb2312") # get the database
        name = database.at[song_index, MAP_NAME] # get the name
        return name
    
    @classmethod
    def getAlias(self, song_index:int) -> list:
        '''
        get the alias of the song as the list form
        
        song_index: the index of the song saved in the MUSIC_PATH csv file
        
        return: the alias of the song as the list form, the cell of the list is str
        '''
        database = pd.read_csv(MUSIC_PATH, encoding="gb2312") # get the database
        column = database.shape[1] # get the total column
        name = database.at[song_index, MAP_NAME] # get the name
        alias=[name]
        for i in range(2, column):
            alias.append(database.iloc[song_index, i])
        return alias
        
    
    @classmethod
    def getRandomClip(self, song_index : int = 0, clip_duration : int = 5) -> str:
        '''
        cut a random clip of the indexth song in the MUSIC_PATH csv file
        
        song_index: the index of the song saved in the MUSIC_PATH csv file
        
        clip_duration: the duration of the output audio file
        
        return: the relative output path of the audio file
        '''
        
        database = pd.read_csv(MUSIC_PATH, encoding="gb2312") # get the MUSIC_PATH database
        
        name = database.at[song_index, MAP_NAME] # get the name
        if str(database.at[song_index, LOBBY])=="nan":
            lobby = 0
        else:
            lobby = int(database.at[song_index, LOBBY]) # 获取路径
        
        music_path = FATHER_PATH + str(lobby) + "/" + str(name) + ".mp4" # "./src/database/music/" + "1" + "/" + "节奏山脊"
        # music_path = FATHER_PATH + str(2) + "/" + str("机制库") + ".mp4" # "./src/database/music/" + "1" + "/" + "机制库"
        if not os.path.exists(music_path):
            return music_path
        audio = AudioSegment.from_file(music_path)
        total_duration = audio.duration_seconds
        rand_start = rd.randint(0, int(total_duration-clip_duration))
        # audio = AudioSegment.from_file(clip_path, format="amr")
        start_time = rand_start * 1000  # 2s
        end_time = (rand_start + clip_duration) * 1000    # 5s
        cropped_audio = audio[start_time:end_time]
        cropped_audio.export(output_path)
        return output_path
        
        
        
