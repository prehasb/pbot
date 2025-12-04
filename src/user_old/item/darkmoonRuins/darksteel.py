from item.item import Item

NAME_IN_USERITEM = "darksteel"
ID = 26

class darksteel(Item):
    item_id = ID
    add_cryph_per_item = 1
    
    def __init__(self, user_id:int):
        super(darksteel, self).__init__(user_id=user_id, item_id=ID)
        
        self._update()
    
    def _update(self):
        super()._update()
    
    # 不可使用
    # def use(self, num):
    #     enough = self.isEnough(num)
        
    #     msg = super().use(num)
    #     if not enough:
    #         return msg
        
    #     return msg
    
    @classmethod
    def describe(self):
        msg = ""
        msg += "\r\n黑钢"
        msg += f"\r\n可以用于加固工厂的机器，每片成品黑钢可以使工厂水晶产出永久+{self.add_cryph_per_item}。"
        return msg
    