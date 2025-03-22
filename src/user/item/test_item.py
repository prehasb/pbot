from item.item import Item

NAME_IN_USERITEM = "test_item"
ITEM_TEST_ID = 0

class test_item(Item):
    item_id = ITEM_TEST_ID
    def __init__(self, user_id:int):
        super(test_item, self).__init__(user_id=user_id, item_id=ITEM_TEST_ID)
        self._update()
    
    def _update(self):
        super()._update()
        
    def use(self, num):
        
        from pet import Pet
        enough = self.isEnough(num)
        
        msg = super().use(num)
        if not enough:
            return msg
        
        get_cry = num*1
        msg += f"你获得了{get_cry}个水晶"
        p = Pet(self.user_id)
        p.giveCry(get_cry)
        
        return msg
    
    @classmethod
    def descripe(self):
        msg = ""
        msg += "\r\n智商检测器"
        msg += "\r\n使用该道具来检测自己的智商吧，使用后可以获得1个水晶哦"
        msg += f"\r\n温馨提示：价格{self.getPrice()}水晶"
        return msg
    