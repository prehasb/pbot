from item.crystalHeart.crystalHeart import crystalHeart
NAME_IN_USERITEM = "crystalHeartStartfruit"

ID = 12
CRY_NUM = 500

class crystalHeartStartfruit(crystalHeart):
    item_id = ID
    gain_cry_per_heart:int = CRY_NUM
    
    def __init__(self, user_id:int):
        super(crystalHeartStartfruit, self).__init__(user_id=user_id, item_id=ID)
        self._update()
    