from item.crystalHeart.crystalHeart import crystalHeart
NAME_IN_USERITEM = "crystalHeartGlide"

# ID = 10
CRY_NUM = 100

class crystalHeartJaded(crystalHeart):
    # item_id = ID
    gain_cry_per_heart:int = CRY_NUM
    
    def __init__(self, user_id:int, item_id:int):
        super(crystalHeartJaded, self).__init__(user_id=user_id, item_id=item_id)
        self._update()
    