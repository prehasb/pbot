from item.item import Item
import datetime as dt
from datetime import datetime

NAME_IN_USERITEM = "herbarium"
ID = 11
TIME_SKIP = 10

class herbarium(Item):
    item_id = ID
    
    def __init__(self, user_id:int):
        super(herbarium, self).__init__(user_id=user_id, item_id=ID)
        self._update()
    
    def _update(self):
        super()._update()
        
    def use(self, num):
        from event.petEvent import petEvent
        
        ev = petEvent(user_id=self.user_id)
        
        enough = self.isEnough(num)
        msg = super().use(num)
        if not enough:
            return msg
        
        current_time = dt.datetime.now()
        time_difference = ev.next_event_time - current_time
        minute_difference = int(time_difference.total_seconds()//60)
        sub_time1 = TIME_SKIP*num
        sub_time2 = (minute_difference * num) // 3
        if sub_time1 > sub_time2:
            sub_time = sub_time1
        else:
            sub_time = sub_time2
        new_delay = minute_difference - sub_time
        ev.setNextTime(new_delay)
        msg += f"信件的时间流速已加速{sub_time}分钟"
        return msg
    
    @classmethod
    def describe(self):
        msg = ""
        msg += "\r\n杨桃星球的植物化石"
        msg += "\r\n杨桃星球到处都是时空紊乱的痕迹，植物化石也是如此。"
        msg += f"\r\n使用后，信件的等待时间减少三分之一或{TIME_SKIP}分钟(取其较大值)。"
        return msg
    