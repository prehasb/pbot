from item.item import Item
NAME_IN_USERITEM = "junkFood"

# ID = 5

class junkFood(Item):
    # item_id = ID
    gain_exp_per_food:int = 1000
    
    def __init__(self, user_id:int, item_id:int):
        super(junkFood, self).__init__(user_id=user_id, item_id=item_id)
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
    
    def getGainExp(self) -> int:
        add_exp = self.gain_exp_per_food
        return add_exp
    
    @classmethod
    def describe(self):
        msg = ""
        msg += "\r\n零食"
        msg += f"\r\n使用后获得{self.gain_exp_per_food}点经验。"
        return msg
    