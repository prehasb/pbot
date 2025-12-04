from item.crystalHeart.crystalHeart import crystalHeart
NAME_IN_USERITEM = "crystalHeartStarfish"

ID = 20
CRY_NUM = 100

class crystalHeartStarfish(crystalHeart):
    item_id = ID
    gain_cry_per_heart:int = CRY_NUM
    
    def __init__(self, user_id:int):
        super(crystalHeartStarfish, self).__init__(user_id=user_id, item_id=ID)
        self._update()
    