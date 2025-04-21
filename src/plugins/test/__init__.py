from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER

prehasb_id = 1019276364

__plugin_meta__ = PluginMetadata(
    name="echo",
    description="重复你说的话",
    usage="/echo [text]",
    type="application",
    config=None,
    supported_adapters=None,
)

echo = on_command("echo")

@echo.handle()
async def handle_echo(event: MessageEvent, message: Message = CommandArg()):
    if any((not seg.is_text()) or str(seg) for seg in message):
        if event.user_id == prehasb_id:
            msg = message
            await echo.send(message=msg)
        else:
            msg = "\0" + message
            await echo.send(message=msg)
        