from item.item import Item
NAME_IN_USERITEM = "expSaveBall"

# ID = 4

class expSaveBall(Item):
    # item_id = ID
    max_exp_per_ball:int = 25000
    gain_exp_per_ball:int = 250000
    
    def __init__(self, user_id:int, item_id:int):
        super(expSaveBall, self).__init__(user_id=user_id, item_id=item_id)
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
        
        get_exp = num*self.getGainExp()
        msg += p.addExp(get_exp)
        
        return msg
    
    def getAddMaxExp(self) -> int:
        max_exp_per_ball = self.max_exp_per_ball
        add_max_exp = self.number * max_exp_per_ball
        return add_max_exp
    
    def getGainExp(self) -> int:
        add_exp_ball = self.gain_exp_per_ball
        return add_exp_ball
    
    @classmethod
    def describe(self):
        msg = ""
        msg += "\r\n经验球"
        msg += f"\r\n持有每个经验球可以增加{self.max_exp_per_ball}点最大存储经验值。"
        msg += f"\r\n经验球也可以被使用，使用后获得{self.gain_exp_per_ball}点经验。"
        return msg
    