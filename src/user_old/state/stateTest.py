from state.stateOperator import State

NAME_IN_USERITEM = "test_item"
ID = 0

class stateTest(State):
    state_id = ID
    def __init__(self, user_id:int):
        super(stateTest, self).__init__(user_id=user_id, state_id=ID)
        self._update()
    
    def _update(self):
        super()._update()
        
    def exist(self, num):
        
        from pet import Pet
        enough = self.isEnough(num)
        
        msg = super().use(num)
        if not enough:
            return msg
        
        get_cry = num*1
        msg += f"你获得了{get_cry}个水晶"
        p = Pet(self.user_id)
        p.addCry(get_cry)
        
        return msg
    
    @classmethod
    def describe(self):
        msg = ""
        msg += "\r\n智商检测器"
        msg += "\r\n使用该道具来检测自己的智商吧，使用后可以获得1个水晶哦"
        msg += f"\r\n温馨提示：价格{self.getPrice()}水晶"
        return msg
    