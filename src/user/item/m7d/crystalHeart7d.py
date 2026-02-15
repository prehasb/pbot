from item.crystalHeart.crystalHeart import crystalHeart
NAME_IN_USERITEM = "crystalHeart7d"

# ID = 18
CRY_NUM = 2000

class crystalHeart7d(crystalHeart):
    # item_id = ID
    gain_cry_per_heart:int = CRY_NUM
    
    def __init__(self, user_id:int):
        super(crystalHeart7d, self).__init__(user_id=user_id, item_id=self.getIdbyEnglishName(self.__class__.__name__))
        self._update()
    