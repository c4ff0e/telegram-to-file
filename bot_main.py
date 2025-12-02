import asyncio
import keyboards
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.types import Message
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os
from dotenv import load_dotenv
import logging
load_dotenv()

class Converter(StatesGroup):
    choice_md = State()
    choice_txt = State()
    wait_for_messages_md = State()
    wait_for_messages_txt = State()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
language = 'ru'
router = Router()

@dp.message(Command("start"), StateFilter(None))
async def start(message: Message):
    await message.answer(
"""
<b>Telegram to .MD 🗨️->🗒️</b>
    
Лёгкий экспорт сообщений в текстовый файл.
Чтобы начать - нажмите на кнопку ниже.
"""
    , reply_markup=keyboards.start_kb)
    
@dp.callback_query(F.data == "start")
async def startagain(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await start(callback.message)


@dp.callback_query(F.data == "cancel")
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await start(callback.message)

async def main():
    import md_helper
    dp.include_router(md_helper.router)
    import txt_helper
    dp.include_router(txt_helper.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())