import keyboards
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.types import Message
from aiogram.types import (                                       
MessageOriginUser, MessageOriginHiddenUser,                   
MessageOriginChannel, MessageOriginChat,)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.types import FSInputFile
from bot_main import Converter
import datetime
import random
router = Router()

@router.callback_query(F.data == "to_md")
async def to_md(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(collected = [])
    await state.set_state(Converter.wait_for_messages_md)
    await callback.message.answer("""
Отправьте сообщения, которые будут экспортированы в файл

<b>ФОРМАТ .md НЕ ПОДДЕРЖИВАЕТ ИЗОБРАЖЕНИЯ. ОНИ БУДУТ ПРОИГНОРИРОВАНЫ.</b>

<b>После отправки напишите команду /done</b>""", reply_markup=keyboards.cancel_kb)

@router.message(Command("done"), Converter.wait_for_messages_md)
async def finish_md(message: Message, state: FSMContext):
    messages = await state.get_data()
    collected = messages.get("collected", [])
    await message.answer(f"Получено {len(collected)} сообщений\n\nХотите добавить больше сообщений?", reply_markup=keyboards.add_more_kb)
    

@router.message(Converter.wait_for_messages_md)
async def collect_messages(message: Message, state: FSMContext):
    messages = await state.get_data()
    collected = messages.get("collected", [])
    collected.append(message)
    await state.update_data(collected = collected)
    
@router.callback_query(Converter.wait_for_messages_md, F.data == "export")
async def export_md(callback: types.CallbackQuery, state: FSMContext):
    gathered = await state.get_data()
    collected = gathered.get("collected", [])
    await state.clear()
    to_export = []
    for message in collected:
        # дата
        if message.date:
            to_export.append(message.date.strftime("%Y-%m-%d %H:%M:%S"))

        # форвард?
        if message.forward_origin:
            origin = message.forward_origin

            if isinstance(origin, MessageOriginUser):
                u = origin.sender_user
                full_name = " ".join(x for x in [u.first_name, u.last_name] if x)
                username = f"@{u.username}" if u.username else ""
                line = f"Переслано от: *{full_name}*"
                if username:
                    line += f", {username}"
                to_export.append(line)

            elif isinstance(origin, MessageOriginHiddenUser):
                # тут только строка имени
                to_export.append(f"Переслано от: *{origin.sender_user_name}*")

            elif isinstance(origin, MessageOriginChannel):
            # сообщение от канала
                chat_title = getattr(origin.chat, "title", None) or "Channel"
                to_export.append(f"Переслано от канала: *{chat_title}*")
            
            elif isinstance(origin, MessageOriginChat):
                chat_title = getattr(origin.chat, "title", None) or "Chat"
                to_export.append(f"Переслано от чата: *{chat_title}*")
            
            else:
                # на всякий случай fallback
                to_export.append("Переслано от: *unknown*")

        else:
            # обычное сообщение (НЕ форвард)
            if message.from_user:
                u = message.from_user
                full_name = " ".join(x for x in [u.first_name, u.last_name] if x)
                username = f"@{u.username}" if u.username else ""
                line = f"От: *{full_name}*"
                if username:
                    line += f", {username}"
                to_export.append(line)
        if message.photo:
            # фото
            if not message.caption:
                to_export.append(f"[Фото]\n")
            elif message.caption:
                to_export.append(f"[Фото]\n")
                to_export.append(message.caption + "\n")
        #документ
        if message.document:
            if not message.caption:
                to_export.append(f"[Файл]: *{message.document.file_name}*\n")
            elif message.caption:
                to_export.append(f"[Файл]: *{message.document.file_name}*")
                to_export.append(message.caption + "\n")
        #видео
        if message.video:
            if not message.caption:
                to_export.append(f"[Видео]: *{message.video.file_name}*\n")
            elif message.caption:
                to_export.append(f"[Видео]: *{message.video.file_name}*")
                to_export.append(message.caption + "\n")
        #аудиофайл
        if message.audio:
            to_export.append(f"[Аудио]: *{message.audio.file_name}*")
            if message.caption:
                to_export.append(message.caption + "\n")
        #кружок
        if message.video_note:
            to_export.append(f"[Кружок]\n")
        #голосовое
        if message.voice:
            to_export.append(f"[Кружок]\n")
        #стикер
        if message.sticker:
            to_export.append(f"[Стикер]: {message.sticker.emoji}\n")
        #контакт
        if message.contact:
            to_export.append(f"[Контакт]: *{message.contact.phone_number}*")
        #чеклист
        if message.checklist:
            to_export.append(f"[Список]:\n**{message.checkkist.title}**")
            for ChecklistTask in message.checklist.tasks:
                to_export.append(f"- {ChecklistTask.text}\n")
        # опрос (господи блять!)
        if message.poll:
            poll = message.poll
            #заголовок
            to_export.append("[Опрос]")
            #вопрос
            to_export.append(f"Вопрос: **{poll.question}**")
            #варианты
            for option in poll.options:
                to_export.append(f"- {option.text} — {option.voter_count} голосов\n")
            # общее количество голосов
            to_export.append(f"Всего голосов: {poll.total_voter_count}")
            # Тип опроса
            if poll.type == "quiz":
                to_export.append("Тип: викторина\n")
                if poll.correct_option_id is not None:
                    correct = poll.options[poll.correct_option_id]
                    to_export.append(f"Правильный ответ: *{correct.text}*\n")
            else:
                to_export.append("Тип: обычный опрос")
            # несколько вариантов
            if poll.allows_multiple_answers:
                to_export.append("Несколько ответов: да")
            else:
                to_export.append("Несколько ответов: нет")
            # обьяснение
            if poll.explanation:
                to_export.append(f"Обьяснение: {poll.explanation}\n")
        
        # текст сообщения
        if message.text:
            to_export.append(message.text + "\n")
    
    await state.clear()
    md_text = "\n".join(to_export)
    filename = f"export{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{random.randint(0, 6767)}.md"
    
    with open (f"{filename}", "w", encoding="utf-8") as f:
        f.write(f"Telegram to .md экспорт {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{md_text}")
    file = FSInputFile(filename)
    await message.answer_document(file)
    await callback.answer()