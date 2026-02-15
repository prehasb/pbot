from item.item import Item
import random as rd

NAME_IN_USERITEM = "theDreamer"
# ID = 28

class theDreamer(Item):
    # item_id = ID
    letter_no_CD_probability_precent = 5
    
    def __init__(self, user_id:int):
        super(theDreamer, self).__init__(user_id=user_id, item_id=self.getIdbyEnglishName(self.__class__.__name__))
        self._update()
    
    def _update(self):
        super()._update()
        randint = rd.randint(0,99)
        self.noCD = False
        if self.number !=0 and randint < self.letter_no_CD_probability_precent:
            self.noCD = True
        
        self.hasCD = not self.noCD
    
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
        msg += "\r\n大梦千秋"
        msg += "\r\n自暗月遗迹恍若大梦的行程中凝结，有些微的概率在梦中完成一次信件传递。"
        # 触发词：你自梦中收到一封信。
        return msg
    
    