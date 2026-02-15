from item.item import Item
NAME_IN_USERITEM = "item1a"

# ID = 6

class item1a(Item):
    # item_id = ID
    
    def __init__(self, user_id:int):
        super(item1a, self).__init__(user_id=user_id, item_id=self.getIdbyEnglishName(self.__class__.__name__))
        self._update()
    
    def _update(self):
        super()._update()
        
    def use(self, num):
        msg = ""
        
        return msg
    
    @classmethod
    def describe(self):
        msg = ""
        msg += "\r\n红绿灯"
        msg += "\r\n1a纪念品"
        return msg
    