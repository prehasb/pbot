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
from item.crystalHeart.crystalHeartSandsofTime import crystalHeartSandsofTime
from item.crystalHeart.crystalHeartShatterSong import crystalHeartShatterSong

# 工厂加工类
from item.mine.unopenedFuel import unopenedFuel
from item.mine.unopenedCrystal import unopenedCrystal

from item.item import Item
ITEM_CLASS_MAPPING:dict[str, Item] = {
    test_item.__name__: test_item,
    expSaveBall.__name__: expSaveBall,
    expEater.__name__: expEater,
    junkFood.__name__: junkFood,
    item1a.__name__: item1a,
    item2a.__name__: item2a,
    herbarium.__name__: herbarium,
    email.__name__ : email,
    reverseButton.__name__: reverseButton,
    proveOfMount.__name__: proveOfMount,
    darksteelRawOre.__name__: darksteelRawOre,
    darksteelFragment.__name__: darksteelFragment,
    darksteel.__name__: darksteel,
    soliteCrystalOre.__name__: soliteCrystalOre,
    luniteCrystalOre.__name__: luniteCrystalOre,
    theDreamer.__name__: theDreamer,
    
    # 水晶之心
    crystalHeart.__name__: crystalHeart,
    crystalHeartGlide.__name__: crystalHeartGlide,
    crystalHeartJaded.__name__: crystalHeartJaded,
    crystalHeartStartfruit.__name__: crystalHeartStartfruit,
    crystalHeartHell.__name__: crystalHeartHell,
    crystalHeartTerminal.__name__: crystalHeartTerminal,
    crystalHeart7d.__name__: crystalHeart7d,
    crystalHeartDreamRidge.__name__: crystalHeartDreamRidge,
    crystalHeartStarfish.__name__: crystalHeartStarfish,
    crystalHeartLostSoul.__name__: crystalHeartLostSoul,
    crystalHeartSuperluminary.__name__: crystalHeartSuperluminary,
    crystalHeartSandsofTime.__name__: crystalHeartSandsofTime,
    crystalHeartShatterSong.__name__: crystalHeartShatterSong,
    
    # 工厂加工
    unopenedFuel.__name__: unopenedFuel,
    unopenedCrystal.__name__: unopenedCrystal,
}


