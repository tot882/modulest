from .. import loader, utils
import asyncio
from asyncio import sleep
from ..inline.types import InlineCall
from telethon.tl.functions.messages import SendMessageRequest
# meta developer: @tot_882 P.S thx @Exttasy1

@loader.tds
class ToTaloil(loader.Module):
    strings = {
        "name": "ToTaloil",
        "delay": "Через сколько минут пробовать качать, если топлива нет?",
        "delay_ex": "Через сколько секунд качать, если топливо есть?",
        "manual_start": "<emoji document_id=5454182632797521992>😱</emoji><b>Качаю нефть.</b><emoji document_id=6334694638359676740>🛢</emoji>",
    }
    
    status = False
    message = ""

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "delay", 60,
                lambda: self.strings["delay"],
                validator=loader.validators.Integer(minimum=60)
            ),
            loader.ConfigValue(
                "delay_ex", 5.0,
                lambda: self.strings["delay_ex"],
                validator=loader.validators.Float(minimum=2.0)
            ),
            loader.ConfigValue(
                "module", True,
                lambda: "da",
                validator=loader.validators.Boolean()
            )
        )

    async def client_ready(self):
        if self.config['module']:
            await self.client.send_message(5522271758, 'Качать')

    @loader.watcher()
    async def WatcherExFuel(self, message):
        exdelay = self.config['delay_ex']
        dela = self.config['delay']
        delay = dela * 60

        if message.raw_text == '❗️В месторождении кончилась нефть!':
            if self.status:
                self.status = False
                await utils.answer(self.message, message.raw_text)
            await asyncio.sleep(delay)
            await self.client.send_message(message.chat_id, 'Качать')
        elif 'Бочка топлива' in message.raw_text:
            if message.chat_id == 5522271758:
                await asyncio.sleep(exdelay)
                await self.client.send_message(message.chat_id, 'Качать')
        elif '❗Хранилище заполнено топливом!' in message.raw_text:
            if self.status:
                self.status = False
                await utils.answer(self.message, message.raw_text)
            await asyncio.sleep(2)
            msg = await self.client.send_message(message.chat_id, "Бур")
            r = await self.client.get_messages(message.chat_id, ids=msg.id)
            await r.click(1)
            r = await self.client.get_messages(message.chat_id, ids=msg.id)
            if '✅' in r.raw_text:
                await asyncio.sleep(delay)
                await self.client.send_message(message.chat_id, 'Качать')
            elif '❗️Авто бур уже заправлен!' in r.raw_text:
                return  # Просто выходим из функции

        if '/checkod' in message.raw_text:
            if message.from_id == 5195118663:
                await self.client.send_message(message.chat_id, 'evo')

    @loader.command("oil", aliases=["Нефть"])
    async def oil(self, message):
        ''''🥰Используй эту команду, чтобы сосать нефть😏'''
        await utils.answer(message, self.strings["manual_start"])
        await self.client.send_message(5522271758, "Качать")
        self.status = True
        self.message = message