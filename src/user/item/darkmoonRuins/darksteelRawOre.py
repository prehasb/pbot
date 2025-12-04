from item.item import Item

NAME_IN_USERITEM = "darksteelRawOre"
# ID = 23

class darksteelRawOre(Item):
    # item_id = ID
    use_number = 5 # 5合1
    process_hour = 2 # 小时
    final_item = "darksteelFragment"
    
    def __init__(self, user_id:int, item_id:int):
        super(darksteelRawOre, self).__init__(user_id=user_id, item_id=item_id)
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
        msg += "\r\n黑钢原矿"
        msg += "\r\n未经提炼的高性能金属原矿，需要提炼后才能使用。"
        msg += f"\r\n{self.use_number}枚原矿可以提炼出足够加固机器的1片黑钢残片。"
        msg += f"\r\n每提炼{self.use_number}枚原矿需要过载工厂{self.process_hour}小时，过载期间无产出。"
        return msg
    