from item.item import Item
NAME_IN_USERITEM = "expSaveBall"

EXPBALL_ID = 4

class expSaveBall(Item):
    item_id = EXPBALL_ID
    max_exp_per_ball:int = 10000
    gain_exp_per_ball:int = 100000
    
    def __init__(self, user_id:int):
        super(expSaveBall, self).__init__(user_id=user_id, item_id=EXPBALL_ID)
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
        
        get_exp = num*self.gain_exp_per_ball
        msg += p.addExp(get_exp)
        
        return msg
    
    def getAddMaxExp(self) -> int:
        add_max_exp = self.number * self.max_exp_per_ball
        return add_max_exp
    
    @classmethod
    def descripe(self):
        msg = ""
        msg += "\r\n经验球"
        msg += "\r\n使用该道具来增加自己的最大存储吧。"
        msg += f"\r\n每个经验球可以增加{self.max_exp_per_ball}点最大存储经验值。"
        return msg
    