from item.item import Item
NAME_IN_USERITEM = "expSaveBall"

EXPBALL_ID = 2

class expEater(Item):
    item_id = EXPBALL_ID
    max_exp_per_ball:int = 10000
    gain_exp_per_ball:int = 100000
    
    def __init__(self, user_id:int):
        super(expEater, self).__init__(user_id=user_id, item_id=EXPBALL_ID)
        self._update()
    
    def _update(self):
        super()._update()
        
    def use(self, num):
        msg = ""
        
        if not self.isEnough(1):
            return "你没有该道具"
        if self.state == 0:
            msg += self.changeState(1)
        elif self.state == 1:
            msg += self.changeState(0)
        
        return msg
    
    def getAddMaxExp(self) -> int:
        add_max_exp = self.number * self.max_exp_per_ball
        return add_max_exp
    
    @classmethod
    def describe(self):
        msg = ""
        msg += "\r\n经验吞噬者"
        msg += "\r\n使用该道具吞噬工厂生产的所有经验。"
        msg += f"\r\n但是吞噬者会多返还给你工厂加工1倍的水晶。"
        return msg
    
    @classmethod
    def getStateName(self, state):
        d = {
            0:"未启用",
            1:"已启用"
            }
        state_name = d[state]
        return state_name
    