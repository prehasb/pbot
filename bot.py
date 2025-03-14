import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotAdapter
from nonebot import get_driver

if __name__ == '__main__':
    nonebot.init()
    driver = get_driver()
    driver.register_adapter(OneBotAdapter)
    nonebot.load_builtin_plugins("echo")
    nonebot.load_plugins('./src/plugins')
    nonebot.run()
