from item.item import Item

NAME_IN_USERITEM = "unopenedFuel"

# ID = 29

class unopenedFuel(Item):
    # item_id = ID
    stone_per_box = 10
    stone_name = "燃料"
    
    def __init__(self, user_id:int):
        super(unopenedFuel, self).__init__(user_id=user_id, item_id=self.getIdbyEnglishName(self.__class__.__name__))
        self._update()
    
    def _update(self):
        super()._update()
        
    def use(self, num):
        enough = self.isEnough(num)
        
        msg = super().use(num)
        if not enough:
            return msg
        
        from user.factory.mine import Mine
        
        m = Mine(self.user_id)
        
        msg += m.give(self.stone_name, self.stone_per_box*num)
        
        return msg
    
    @classmethod
    def describe(self):
        msg = ""
        msg += f"\r\n装有{self.stone_name}的箱子"
        msg += f"\r\n使用后可以获得{self.stone_per_box}份{self.stone_name}"
        return msg
    
    