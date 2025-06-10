# 在此注册所有道具
from item.test_item import test_item
from item.expSaveBall import expSaveBall
from item.expEater import expEater
from item.junkFood import junkFood
from item.item1a import item1a
from item.item2a import item2a
from item.email import email
from item.starfruit.herbarium import herbarium
from item.m7d.proveOfMount import proveOfMount

# 水晶之心
from item.crystalHeart.crystalHeart import crystalHeart
from item.crystalHeart.crystalHeartGlide import crystalHeartGlide
from item.crystalHeart.crystalHeartJaded import crystalHeartJaded
from item.starfruit.crystalHeartStartfruit import crystalHeartStartfruit
from item.hell.crystalHeartHell import crystalHeartHell
from item.crystalHeart.crystalHeartTerminal import crystalHeartTerminal
from item.reverseButton import reverseButton
from item.m7d.crystalHeart7d import crystalHeart7d
from item.crystalHeart.crystalHeartDreamRidge import crystalHeartDreamRidge
from item.crystalHeart.crystalHeartStarfish import crystalHeartStarfish

from item.item import Item
ITEM_CLASS_MAPPING:dict[str, Item] = {
    "test_item": test_item,
    "expSaveBall": expSaveBall,
    "expEater": expEater,
    "junkFood": junkFood,
    "item1a": item1a,
    "item2a": item2a,
    "herbarium": herbarium,
    "email" : email,
    "reverseButton": reverseButton,
    "proveOfMount": proveOfMount,
    
    # 水晶之心
    "crystalHeart": crystalHeart,
    "crystalHeartGlide": crystalHeartGlide,
    "crystalHeartJaded": crystalHeartJaded,
    "crystalHeartStartfruit": crystalHeartStartfruit,
    "crystalHeartHell": crystalHeartHell,
    "crystalHeartTerminal": crystalHeartTerminal,
    "crystalHeart7d": crystalHeart7d,
    "crystalHeartDreamRidge": crystalHeartDreamRidge,
    "crystalHeartStarfish": crystalHeartStarfish,
}


