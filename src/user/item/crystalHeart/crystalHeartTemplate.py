from item.crystalHeart.crystalHeart import crystalHeart

# 整个道具完成情况：()

NAME_IN_USERITEM = "name" # 填写英文名称 完成情况：()
# ID = -1 # 填写ID 完成情况：()
CRY_NUM = -1 # 填写水晶数量 完成情况：()

#########################
# 在 itemRegistor 注册该类 完成情况: ()
# 在 item_table 注册该类 完成情况: ()
#########################

class name(crystalHeart): # 修改类名 完成情况：()
    # item_id = ID
    gain_cry_per_heart:int = CRY_NUM
    
    def __init__(self, user_id:int, item_id:int):
        super(name, self).__init__(user_id=user_id, item_id=item_id) # 修改类名 完成情况：()
        self._update()
    