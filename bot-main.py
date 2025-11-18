import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
import os
from dotenv import load_dotenv
import logging
load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
    """
    Telegram to .MD 🗨️->🗒️
    
    
    """
    )
    

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())