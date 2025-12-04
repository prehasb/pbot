from item.crystalHeart.crystalHeart import crystalHeart
NAME_IN_USERITEM = "crystalHeartTerminal"

ID = 15
CRY_NUM = 50

class crystalHeartTerminal(crystalHeart):
    item_id = ID
    gain_cry_per_heart:int = CRY_NUM
    
    def __init__(self, user_id:int):
        super(crystalHeartTerminal, self).__init__(user_id=user_id, item_id=ID)
        self._update()
    