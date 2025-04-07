import pandas as pd
import numpy as np  # 用于生成 NaN 值

DATABASE_PATH = "./src/database/database.csv"

# 定义column数据
USER_ID = "id"
PET_HAPPINESS = 3
PET_HUNGRY = 4
PET_WATER = 5
PET_LEVEL = 6
PET_EXP = 7
PET_MAXEXP = 8

class User(object):
    user_id : int
    '''用户id'''
    user_row : int
    '''用户所在行'''
    
    def __init__(self, user_id : int, database_path : str = DATABASE_PATH):
        super(User, self).__init__()
        self.user_id = user_id
        self.database_path = database_path
        self.row = None
        
        database = pd.read_csv(self.database_path) # pandas读取操作，现在database是一个矩阵
        # database: (example)
        #   col1  col2
        # 0  1     2
        # 1  3     4
        # 2  5     6
        
        total_line = database.shape[0]
        # database.shape: (3,  2)
        #                 (行, 列)
        find_user = False
        for row in range(0, total_line): # row = 0, 1, 2
            if self.user_id == database.iloc[row, 0]: # 3(self.user_id) == 3(database.iloc[1, 0])
                self.row = row # self.row = 1
                find_user = True
                break
        if not find_user: # if self.row == 2
            self._createNewUser() # 添加用户
            self.row = total_line

    
    def __str__(self) -> str:
        return f"行:{self.row}\r\n用户id:{self.user_id}\r\n"
    
    def read(self, column:str):
        print(f"read column: {column}")
        database = pd.read_csv(self.database_path)
        data = database.at[self.row, column]
        if str(data) == 'nan':
            return None
        return data
        
    def _update(self):
        '''更新自己的状态'''
        pass
        
    def set_next_time(self):
        pass
    
    def _createNewUser(self):
        db = pd.read_csv(self.database_path)
        # db: (example)
        #    id  col2
        # 0  1     2
        # 1  3     4
        # 2  5     6
        # 3  9     9
        
        # 1、创建一个新行，只有id列不为空
        new_row = {"id": self.user_id}
        for col in db:
            if(col not in new_row):
                new_row[col] = np.nan
        # new_row: {"id": self.user_id, "col2": nan}
        
        df_new = pd.DataFrame([new_row])
        # df_new: (example) (self.id == 10)
        #    id  col2
        # 0  10  nan
        
        df_combined = pd.concat([db, df_new], ignore_index=True)
        # df_combined: (example)
        #    id  col2
        # 0  1     2
        # 1  3     4
        # 2  5     6
        # 3  9     9
        # 4  10   nan
        
        df_combined.to_csv(self.database_path, index = False)
    
    def write(self, column:str, data) -> bool:
        '''向数据库内填写数据，同时更新自己的状态'''
        
        print(f"write column: {column}, data: {data}")
        
        if self.row == None:
            return False
        
        
        database = pd.read_csv(self.database_path)
        database.at[self.row, column] = data
        database.to_csv(self.database_path, index=False)
        # self._update()
        return True






