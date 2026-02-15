from item.item import Item
NAME_IN_USERITEM = "proveOfMount"

# ID = 17
MULTI = 2

class proveOfMount(Item):
    # item_id = ID
    multi = MULTI
    
    def __init__(self, user_id:int):
        super(proveOfMount, self).__init__(user_id=user_id, item_id=self.getIdbyEnglishName(self.__class__.__name__))
        self._update()
    
    def _update(self):
        super()._update()
        
    def use(self, num):
        msg = f"不可使用该道具{self.getName()}"
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
        msg += "\r\n登山之证"
        msg += f"\r\n是登上某座高山的证明。"
        msg += f"\r\n持有这个证明，每日jrrp时，可以获得{MULTI}倍的经验。"
        return msg
    