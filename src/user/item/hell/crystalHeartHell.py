from item.crystalHeart.crystalHeart import crystalHeart
NAME_IN_USERITEM = "crystalHeartHell"

# ID = 14
CRY_NUM = 500

class crystalHeartHell(crystalHeart):
    # item_id = ID
    gain_cry_per_heart:int = CRY_NUM
    
    def __init__(self, user_id:int):
        super(crystalHeartHell, self).__init__(user_id=user_id, item_id=self.getIdbyEnglishName(self.__class__.__name__))
        self._update()
    