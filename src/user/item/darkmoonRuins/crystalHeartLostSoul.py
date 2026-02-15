from item.crystalHeart.crystalHeart import crystalHeart
NAME_IN_USERITEM = "crystalHeartLostSoul"

# ID = 22
CRY_NUM = 2000

class crystalHeartLostSoul(crystalHeart):
    # item_id = ID
    gain_cry_per_heart:int = CRY_NUM
    
    def __init__(self, user_id:int):
        super(crystalHeartLostSoul, self).__init__(user_id=user_id, item_id=self.getIdbyEnglishName(self.__class__.__name__))
        self._update()
    