from item.item import Item

# ID = 13
SKIP_MINUTE = 5

class email(Item):
    # item_id = ID
    skip_minute = SKIP_MINUTE
    
    def __init__(self, user_id:int, item_id:int):
        super(email, self).__init__(user_id=user_id, item_id=item_id)
        self._update()
    
    def _update(self):
        super()._update()
        
    def use(self, num):
        msg = "不可使用该道具[电子邮件]"
        return msg
    
    @classmethod
    def describe(self):
        msg = ""
        msg += "\r\n电子邮件"
        msg += f"\r\n略微增加玛德琳回信的速度，使玛德琳回信的速度降低{self.skip_minute}分钟"
        msg += f"\r\n或许除了购买，还有其他的获取方式？"
        return msg
    