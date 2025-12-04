import pandas as pd

GLOBAL_PATH = "./src/database/global.csv"

class Global(object):
    
    database_path = GLOBAL_PATH
    
    def __init__(self, database_path : str = GLOBAL_PATH):
        super().__init__()
        self.database_path = database_path
    
    @classmethod
    def read(self, column:str):
        print(f"read column: {column}")
        database = pd.read_csv(self.database_path)
        data = database.at[0, column]
        if str(data) == 'nan':
            return None
        return data
    
    @classmethod
    def write(self, column:str, data) -> bool:
        '''向数据库内填写数据'''
        print(f"write column: {column}, data: {data}")
        database = pd.read_csv(self.database_path)
        database.at[0, column] = data
        database.to_csv(self.database_path, index=False)
    
    
    