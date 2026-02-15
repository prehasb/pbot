from item.item import Item
NAME_IN_USERITEM = "reverseButton"

# ID = 16

class reverseButton(Item):
    # item_id = ID
    
    def __init__(self, user_id:int):
        super(reverseButton, self).__init__(user_id=user_id, item_id=self.getIdbyEnglishName(self.__class__.__name__))
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
    
    @classmethod
    def describe(self):
        msg = ""
        msg += "\r\n反转按钮"
        msg += "\r\n是来自反转山脊的特殊按钮"
        msg += f"\r\n使用之后，工厂每秒加工的经验和每小时加工的水晶数量调换"
        msg += f"\r\n除了购买之外，还可以让玛德琳从反转山脊给你带回来"
        return msg
    
    @classmethod
    def getStateName(self, state):
        d = {
            0:"未启用",
            1:"已反转"
            }
        state_name = d[state]
        return state_name
    