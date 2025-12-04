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
from item.darkmoonRuins.darksteelRawOre import darksteelRawOre
from item.darkmoonRuins.darksteelFragment import darksteelFragment
from item.darkmoonRuins.darksteel import darksteel
from item.darkmoonRuins.soliteCrystalOre import soliteCrystalOre
from item.darkmoonRuins.luniteCrystalOre import luniteCrystalOre
from item.darkmoonRuins.theDreamer import theDreamer

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
from item.darkmoonRuins.crystalHeartLostSoul import crystalHeartLostSoul
from item.crystalHeart.crystalHeartSuperluminary import crystalHeartSuperluminary

# 工厂加工类
from item.mine.unopenedFuel import unopenedFuel
from item.mine.unopenedCrystal import unopenedCrystal

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
    "darksteelRawOre": darksteelRawOre,
    "darksteelFragment": darksteelFragment,
    "darksteel": darksteel,
    "soliteCrystalOre": soliteCrystalOre,
    "luniteCrystalOre": luniteCrystalOre,
    "theDreamer": theDreamer,
    
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
    "crystalHeartLostSoul": crystalHeartLostSoul,
    "crystalHeartSuperluminary": crystalHeartSuperluminary,
    
    # 工厂加工
    "unopenedFuel": unopenedFuel,
    "unopenedCrystal": unopenedCrystal,
}


