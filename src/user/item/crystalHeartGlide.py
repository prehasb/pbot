from item.crystalHeart import crystalHeart
NAME_IN_USERITEM = "crystalHeartGlide"

ID = 9
CRY_NUM = 50
NAME = "水晶之心：雨落玫瑰"

class crystalHeartGlide(crystalHeart):
    item_id = ID
    gain_cry_per_heart:int = CRY_NUM
    name = NAME
    
    def __init__(self, user_id:int):
        super(crystalHeartGlide, self).__init__(user_id=user_id, item_id=ID)
        self._update()
    