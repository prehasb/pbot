from item.item import Item

# 整个道具 完成情况：()

NAME_IN_USERITEM = "darksteelFragment"
ID = 24

class darksteelFragment(Item):
    item_id = ID
    use_number = 4 # 合1
    process_hour = 1 # 小时
    final_item = "darksteel"
    
    def __init__(self, user_id:int):
        super(darksteelFragment, self).__init__(user_id=user_id, item_id=ID)
        self._update()
    
    def _update(self):
        super()._update()
    
    def use(self, num):
        enough = self.isEnough(num*self.use_number)
        
        from user.state.stateOperator import stateOperator
        so = stateOperator(self.user_id)
        if so.exist("factoryStop"):
            msg += "无法加工，工厂正处于停滞状态"
            return msg
        
        msg = super().use(num*self.use_number)
        if not enough:
            return msg
        
        so.giveState("factoryStop", hours=num*self.process_hour)
        so.giveState(self.getNameinUseritem() + "Processing", hours=num*self.process_hour)
        
        from user.factory.factory import Factory
        fac = Factory(self.user_id)
        fac.delayFactoryTime(hours=num*self.process_hour)
        
        from user.item.itemOperation import ItemOperation
        io = ItemOperation(self.user_id)
        msg += f"\r\n已使用{num*self.use_number}个{self.getName()}"
        msg += io.give(ItemOperation.getNamebyNameInUseritem(self.final_item), num)
        msg += f"\r\n注意，工厂生产将停滞{num*self.process_hour}小时！"
        
        return msg
    
    @classmethod
    def describe(self):
        msg = ""
        msg += "\r\n黑钢残片"
        msg += "\r\n遗迹中脱落的黑钢碎片，无法直接使用。"
        msg += f"\r\n{self.use_number}片残片可以重铸出1片成品黑钢。"
        msg += f"\r\n每重铸{self.use_number}片残片需过载工厂{self.process_hour}小时，过载期间无产出。"
        return msg
    
    #########################
    # 在此处定义道具的其他行为 完成情况：()
    #########################
    