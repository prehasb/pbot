from item.crystalHeart.crystalHeart import crystalHeart
NAME_IN_USERITEM = "crystalHeartDreamRidge"

# ID = 19
CRY_NUM = 50

class crystalHeartDreamRidge(crystalHeart):
    # item_id = ID
    gain_cry_per_heart:int = CRY_NUM
    
    def __init__(self, user_id:int, item_id:int):
        super(crystalHeartDreamRidge, self).__init__(user_id=user_id, item_id=item_id)
        self._update()
    