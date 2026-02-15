from item.item import Item

# ID = 8
CRY_NUM = 50

class crystalHeart(Item):
    # item_id = ID
    gain_cry_per_heart:int = CRY_NUM
    
    
    def __init__(self, user_id:int, item_id=-1):
        if item_id == -1:
            item_id = self.getIdbyEnglishName(self.__class__.__name__)
        super(crystalHeart, self).__init__(user_id=user_id, item_id=item_id)
        self._update()
    
    def _update(self):
        super()._update()
        
    def use(self, num):
        from pet import Pet
        enough = self.isEnough(num)
        
        msg = super().use(num)
        if not enough:
            return msg
        
        p = Pet(self.user_id)
        
        get_cry = num*self.getGainCry()
        msg += p.addCry(get_cry)
        
        return msg
    
    def getGainCry(self) -> int:
        add_exp_ball = self.gain_cry_per_heart
        return add_exp_ball
    
    @classmethod
    def describe(self):
        msg = ""
        msg += f"\r\n{self.getName()}"
        msg += f"\r\n使用后获得{self.gain_cry_per_heart}个水晶。"
        return msg

# 水晶之心子类



