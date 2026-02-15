from item.crystalHeart.crystalHeart import crystalHeart

# 整个道具完成情况：()

CRY_NUM = -1 # 填写水晶数量 完成情况：()

#########################
# 在 itemRegistor 注册该类 完成情况: ()
# 在 item_table 注册该类 完成情况: ()
#########################

class name(crystalHeart): # 修改类名 完成情况：()
    gain_cry_per_heart:int = CRY_NUM
    
    def __init__(self, user_id:int):
        super(self.__class__, self).__init__(user_id=user_id, item_id=self.getIdbyEnglishName(self.__class__.__name__))
        self._update()
    