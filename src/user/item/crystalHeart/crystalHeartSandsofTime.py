from item.crystalHeart.crystalHeart import crystalHeart

CRY_NUM = 50

class crystalHeartSandsofTime(crystalHeart):
    gain_cry_per_heart:int = CRY_NUM
    
    def __init__(self, user_id:int):
        super(self.__class__, self).__init__(user_id=user_id, item_id=self.getIdbyEnglishName(self.__class__.__name__))
        self._update()
    