# 在此注册所有道具
from item.test_item import test_item
from item.expSaveBall import expSaveBall
from item.expEater import expEater
from item.junkFood import junkFood
from item.item1a import item1a
from item.item2a import item2a
from item.crystalHeart import crystalHeart
from item.crystalHeartGlide import crystalHeartGlide
from item.crystalHeartJaded import crystalHeartJaded

from item.item import Item

ITEM_CLASS_MAPPING:dict[str, Item] = {
    "test_item": test_item,
    "expSaveBall": expSaveBall,
    "expEater": expEater,
    "junkFood": junkFood,
    "item1a": item1a,
    "item2a": item2a,
    "crystalHeart": crystalHeart,
    "crystalHeartGlide": crystalHeartGlide,
    "crystalHeartJaded": crystalHeartJaded,
}

ITEM_IN_LETTER:list = {
    "test_item",
    "expSaveBall",
    "crystalHeartGlide",
    "crystalHeartJaded",
}


