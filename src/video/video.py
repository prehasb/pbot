import random as rd
from pydub import AudioSegment
import pandas as pd
import time as tm
import os

 
# 设置文件路径
OUTPUT_PATH = './src/database/music/output.amr'  # 输出MP4文件路径

MUSIC_PATH = '/music.csv'

FATHER_PATH = "./src/database/music/"

SONG_NAME = "song_name"
LOBBY = "lobby"

# music_dict
MYSIC_TYPE = "music_type"
MUSIC_ID = "music_id"
MUSIC_TIME = "music_time"

class RandomVideo(object):
    duration:int
    '''时间长度'''
    begin:int
    '''开始时间'''
    filepath:str
    '''文件位置'''
    
    def __init__(self, music_dict:dict):
        super(RandomVideo, self).__init__()
        self.music_dict = music_dict
    
    def getRandomIndex(self) -> int:
        # "./src/database/music/" + "celeste" + '/music.csv'
        database = pd.read_csv(FATHER_PATH + self.music_dict[MYSIC_TYPE] + MUSIC_PATH, encoding="gb2312") # get the database
        total_line = database.shape[0] # total row
        
        time = tm.time_ns()
        rd.seed(time)
        song_index = rd.randint(0,total_line-1) # pick a random song index
        return song_index
    
    def getName(self, song_index:int) -> str:
        '''获取获取对应下标歌曲的alias列表List
        
        @param: song_index MUSIC_PATH的csv文件中的歌曲下标'''
        # "./src/database/music/" + "celeste" + '/music.csv'
        database = pd.read_csv(FATHER_PATH + self.music_dict[MYSIC_TYPE] + MUSIC_PATH, encoding="gb2312") # get the database
        name = database.at[song_index, SONG_NAME] # get the name
        return name
    
    def getAlias(self, song_index:int) -> list:
        '''
        get the alias of the song as the list form
        
        song_index: the index of the song saved in the MUSIC_PATH csv file
        
        return: the alias of the song as the list form, the cell of the list is str
        '''
        # "./src/database/music/" + "celeste" + '/music.csv'
        database = pd.read_csv(FATHER_PATH + self.music_dict[MYSIC_TYPE] + MUSIC_PATH, encoding="gb2312") # get the database
        column = database.shape[1] # get the total column
        name = database.at[song_index, SONG_NAME] # get the name
        alias=[name]
        for i in range(2, column):
            alias.append(database.iloc[song_index, i])
        return alias
    
    # @classmethod
    # def getClip(self, name : str|None = None, clip_duration : int = 5) -> str:
    #     music_path = FATHER_PATH + self.music_dict[MYSIC_TYPE] + "/" + str(name) + ".mp4" # "./src/database/music/" + "1" + "/" + "节奏山脊"
    #     if not os.path.exists(music_path):
    #         return music_path
    #     audio = AudioSegment.from_file(music_path)
    #     total_duration = audio.duration_seconds
    #     if clip_duration == -1:
    #         cropped_audio = audio[0:total_duration*1000]
    #         cropped_audio.export(OUTPUT_PATH)
    #         return OUTPUT_PATH
    #     rand_start = rd.randint(0, int(total_duration-clip_duration))
    #     # audio = AudioSegment.from_file(clip_path, format="amr")
    #     start_time = rand_start * 1000  # 2s
    #     end_time = (rand_start + clip_duration) * 1000    # 5s
    #     cropped_audio = audio[start_time:end_time]
    #     cropped_audio.export(OUTPUT_PATH)
    #     return OUTPUT_PATH

    def getIndexByName(self, name : str) -> int:
        # "./src/database/music/" + "celeste" + '/music.csv'
        df = pd.read_csv(FATHER_PATH + self.music_dict[MYSIC_TYPE] + MUSIC_PATH, encoding="gb2312")
        for row_idx, row in df.iterrows():
            for col_idx, cell in enumerate(row):
                if str(cell) == str(name):
                    return row_idx
        return 0

    @classmethod
    def getRandomClip(self, song_index : int = 0, clip_duration : int = 5) -> str:
        '''
        cut a random clip of the indexth song in the MUSIC_PATH csv file
        
        song_index: the index of the song saved in the MUSIC_PATH csv file
        
        clip_duration: the duration of the output audio file, -1 for all clip
        
        return: the relative output path of the audio file
        '''
        # "./src/database/music/" + "celeste" + '/music.csv'
        database = pd.read_csv(FATHER_PATH + self.music_dict[MYSIC_TYPE] + MUSIC_PATH, encoding="gb2312") # get the MUSIC_PATH database
        
        name = database.at[song_index, SONG_NAME] # get the name
        if str(database.at[song_index, LOBBY])=="nan":
            lobby = 0
        else:
            lobby = int(database.at[song_index, LOBBY]) # 获取路径
        
        # "./src/database/music/" + "celeste" + "/" + "1" + "/" + <name> + '.mp4'
        music_path = FATHER_PATH + self.music_dict[MYSIC_TYPE] + "/" + str(lobby) + "/" + str(name) + ".mp4"
        if not os.path.exists(music_path):
            return music_path
        audio = AudioSegment.from_file(music_path)
        total_duration = audio.duration_seconds
        if clip_duration == -1:
            cropped_audio = audio[0:total_duration*1000]
            cropped_audio.export(OUTPUT_PATH) # TODO output path加随机数避免冲突
            return OUTPUT_PATH
        rand_start = rd.randint(0, int(total_duration-clip_duration))
        # audio = AudioSegment.from_file(clip_path, format="amr")
        start_time = rand_start * 1000  # 2s
        end_time = (rand_start + clip_duration) * 1000    # 5s
        cropped_audio = audio[start_time:end_time]
        cropped_audio.export(OUTPUT_PATH)
        return OUTPUT_PATH
        
        
        
