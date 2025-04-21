from item.item import Item

NAME_IN_USERITEM = "herbarium"
ID = 11

class herbarium(Item):
    item_id = ID
    
    def __init__(self, user_id:int):
        super(herbarium, self).__init__(user_id=user_id, item_id=ID)
        self._update()
    
    def _update(self):
        super()._update()
        
    def use(self, num):
        
        msg = "暂时无法使用该道具"
        return msg
        
        from pet import Pet
        enough = self.isEnough(num)
        
        msg = super().use(num)
        if not enough:
            return msg
        
        p = Pet(self.user_id)
        
        get_exp = num*self.getGainExp()
        msg += p.addExp(get_exp)
        
        return msg
    
    @classmethod
    def describe(self):
        msg = ""
        msg += "\r\n杨桃星球的植物化石"
        return msg
        # TODO
        msg += "\r\n杨桃星球到处都是时空紊乱的痕迹，植物化石也是如此。"
        msg += "\r\n使用后，工厂1天内水晶产量翻倍。"
        return msg
    