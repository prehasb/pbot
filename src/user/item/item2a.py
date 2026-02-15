from item.item import Item
NAME_IN_USERITEM = "item2a"

# ID = 7

class item2a(Item):
    # item_id = ID
    max_exp_per_ball:int = 10000
    gain_exp_per_ball:int = 100000
    
    def __init__(self, user_id:int):
        super(item2a, self).__init__(user_id=user_id, item_id=self.getIdbyEnglishName(self.__class__.__name__))
        self._update()
    
    def _update(self):
        super()._update()
        
    def use(self, num):
        msg = ""
        
        return msg
    
    @classmethod
    def describe(self):
        msg = ""
        msg += "\r\n果冻"
        msg += "\r\n2a纪念品"
        return msg
    
    