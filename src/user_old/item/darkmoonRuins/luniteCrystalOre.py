from item.item import Item

# 整个道具 完成情况：()

NAME_IN_USERITEM = "luniteCrystalOre"
ID = 25

class luniteCrystalOre(Item):
    item_id = ID
    get_cry_hour = 4
    
    def __init__(self, user_id:int):
        super(luniteCrystalOre, self).__init__(user_id=user_id, item_id=ID)
        self._update()
    
    def _update(self):
        super()._update()
        
    def use(self, num):
        enough = self.isEnough(num)
        
        msg = super().use(num)
        if not enough:
            return msg
        
        from user.factory.factory import Factory
        fac = Factory(self.user_id)
        
        msg += fac.updateExpandCry()
        
        from user.state.stateOperator import stateOperator
        so = stateOperator(self.user_id)
        so.giveState("luniteCrystalOre", hours = self.get_cry_hour)
        so.giveState("factoryDouble", hours = self.get_cry_hour)
        
        msg += f"\r\n已使用{num}个{self.getName()}，"
        msg += f"\r\n接下来{num*self.get_cry_hour}小时内，从工厂中取出的物品翻倍。"
        
        #########################
        # 在此处定义道具使用的方式 完成情况：()
        #########################
        
        return msg
    
    @classmethod
    def describe(self):
        msg = ""
        msg += "\r\n皎寒水晶原矿"
        msg += "\r\n极难开采的优质水晶矿石，尽管不能用于供能，但可以和烈冕水晶发生特殊反应生成时空虫洞。"
        msg += "\r\n切记，纯度不足的水晶反应将产生黑洞。"
        msg += f"\r\n可用做冷却装置，使工厂无副作用过载{self.get_cry_hour}小时，过载期间收获翻倍。"
        msg += "\r\n用于过载加工黑钢时可使加工时间产量翻倍。一枚水晶只能用于一次加工。"
        return msg
    
    #########################
    # 在此处定义道具的其他行为 完成情况：()
    #########################
    