import pandas as pd
from User import User
from datetime import datetime
import datetime as dt

GLOBAL_PATH = "./src/database/global.csv"
MUSIC = "music"

DEFAULT_MUSIC_DICT = {
    "music_type":"celeste",
    "index_now":0,
    "guess_state":False, 
    "total_ans":0,
    "begin_time":datetime.now() - dt.timedelta(seconds=30),
}

class Global(User):
    
    database_path = GLOBAL_PATH
    
    def __init__(self, group_id : int, database_path : str = GLOBAL_PATH):
        super().__init__(user_id=group_id, database_path=GLOBAL_PATH)
        self.database_path = database_path
    
    def getMusicDict(self) -> dict:
        music_string = self.read(MUSIC)
        if music_string == None or music_string == '':
            music_dict = DEFAULT_MUSIC_DICT
            self.setMusicDict(music_dict)
        else:
            music_dict = self.str2Dict(music_string)
        return music_dict
        
    def setMusicDict(self, music_dict:dict):
        music_string = self.dict2Str(music_dict)
        self.write(MUSIC, music_string)
    # @classmethod
    # def read(self, column:str):
    #     print(f"read column: {column}")
    #     database = pd.read_csv(self.database_path)
    #     data = database.at[0, column]
    #     if str(data) == 'nan':
    #         return None
    #     return data
    
    # 以下是辅助函数
    def str2Dict(self, s:str) -> dict[str, int]:
        '''将字符串 s="a:123|b:456" 变为字典 d={"a":123, "b":456} '''
        if not s:
            return dict()
        
        str_list = s.split("|") # ["a:123", "b:456"]
        typelist:type = [str, int, bool, int, datetime]
        d = dict() 
        
        for i in range(len(str_list)):
            parts = str_list[i].split(':', 1) # parts = ["a","123"]
            if len(parts) == 2:
                if typelist[i] == int:
                    d[parts[0]] = typelist[i](parts[1])
                elif typelist[i] == bool:
                    if parts[1].lower() == "true":
                        d[parts[0]] = True
                    else:
                        d[parts[0]] = False
                elif typelist[i] == datetime:
                    d[parts[0]] = datetime.strptime(parts[1], "%Y-%m-%d %H:%M:%S.%f")
                else: 
                    d[parts[0]] = typelist[i](parts[1])
        return d

    # @classmethod
    # def write(self, column:str, data) -> bool:
    #     '''向数据库内填写数据'''
    #     print(f"write column: {column}, data: {data}")
    #     database = pd.read_csv(self.database_path)
    #     database.at[0, column] = data
    #     database.to_csv(self.database_path, index=False)
    
    # @classmethod
    # def getTypeOfGroup(self, group_id, column):
    #     database = pd.read_csv(self.database_path)
    #     row = database[database["group_id"] == group_id]
    #     return row
        
    # @classmethod
    # def getRowOf(self, group_id):
    #     database = pd.read_csv(self.database_path)
    #     row = database[database["group_id"] == group_id]
    #     return row
    
    # @classmethod
    # def isPet(self, group_id):
    #     row = self.getRowOf(group_id)
    #     self.read()
    
    
    