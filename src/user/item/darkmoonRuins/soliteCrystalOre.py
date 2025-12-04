from item.item import Item

# 整个道具 完成情况：()

NAME_IN_USERITEM = "soliteCrystalOre"
ID = 27
# 
class soliteCrystalOre(Item):
    # item_id = ID
    get_cry_hour = 3
    
    def __init__(self, user_id:int, item_id:int):
        super(soliteCrystalOre, self).__init__(user_id=user_id, item_id=item_id)
        self._update()
    
    def _update(self):
        super()._update()
        
    def use(self, num):
        
        from user.state.stateOperator import stateOperator
        so = stateOperator(self.user_id)
        
        if so.exist("luniteCrystalOre"):
            msg = "\r\n烈冕水晶原矿无法与与皎寒水晶一起使用"
            return msg
        
        enough = self.isEnough(num)
        
        msg = super().use(num)
        if not enough:
            return msg
        
        from user.pet import Pet
        from item.reverseButton import reverseButton
        from user.factory.factory import Factory
        
        p = Pet(self.user_id)
        button = reverseButton(self.user_id)
        fac = Factory(self.user_id)
        
        cryph = fac.getFacrotyCryPh(eater_flag=False, button_flag=False)
        
        # 反转按钮：若反转，则获得3h经验
        if button.state == 0:
            msg += p.addCry(cryph*self.get_cry_hour)
        if button.state == 1:
            msg += p.addExp(cryph*self.get_cry_hour*3600)
        
        return msg
    
    @classmethod
    def describe(self):
        msg = ""
        msg += "\r\n烈冕水晶原矿"
        msg += "\r\n珍贵的能源水晶原矿，能够提供高效的能源。"
        msg += "\r\n不建议与皎寒水晶一起储存，否则将产生灾难性的后果。"
        msg += f"\r\n使用后直接获得工厂{self.get_cry_hour}h的产出，不受经验吞噬者影响。"
        return msg
    
