# 在此注册所有状态
from item.test_item import test_item
from item.expSaveBall import expSaveBall
from item.expEater import expEater
from item.junkFood import junkFood
from item.item1a import item1a
from item.item2a import item2a
from item.crystalHeart.crystalHeart import crystalHeart
from item.crystalHeart.crystalHeartGlide import crystalHeartGlide
from item.crystalHeart.crystalHeartJaded import crystalHeartJaded
from item.starfruit.herbarium import herbarium
from item.starfruit.crystalHeartStartfruit import crystalHeartStartfruit

from item.item import Item

STATE_CLASS_MAPPING:dict[str, Item] = {
    "test_item": test_item,
    "expSaveBall": expSaveBall,
    "expEater": expEater,
    "junkFood": junkFood,
    "item1a": item1a,
    "item2a": item2a,
    "crystalHeart": crystalHeart,
    "crystalHeartGlide": crystalHeartGlide,
    "crystalHeartJaded": crystalHeartJaded,
    "herbarium": herbarium,
    "crystalHeartStartfruit": crystalHeartStartfruit,
}


