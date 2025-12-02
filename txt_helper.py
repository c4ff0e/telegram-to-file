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
import os
router = Router()

@router.callback_query(F.data == "to_txt")
async def to_txt(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(collected = [])
    await state.set_state(Converter.wait_for_messages_txt)
    await callback.message.answer("""
Отправьте сообщения, которые будут экспортированы в файл

<b>ФОРМАТ .txt НЕ ПОДДЕРЖИВАЕТ ИЗОБРАЖЕНИЯ, ВИДЕО, АУДИОФАЙЛЫ. ОНИ БУДУТ ПРОИГНОРИРОВАНЫ.</b>

После отправки напишите команду /done""", reply_markup=keyboards.cancel_kb)

@router.message(Command("done"), Converter.wait_for_messages_txt)
async def finish_txt(message: Message, state: FSMContext):
    messages = await state.get_data()
    collected = messages.get("collected", [])
    await message.answer(f"Получено {len(collected)} сообщений\n\nХотите добавить больше сообщений?", reply_markup=keyboards.add_more_kb)


@router.message(Converter.wait_for_messages_txt)
async def collect_messages(message: Message, state: FSMContext):
    messages = await state.get_data()
    collected = messages.get("collected", [])
    collected.append(message)
    await state.update_data(collected = collected)

@router.callback_query(Converter.wait_for_messages_txt, F.data == "export")
async def export_txt(callback: types.CallbackQuery, state: FSMContext):
    gathered = await state.get_data()
    collected = gathered.get("collected", [])
    await state.clear()
    to_export = []
    for i, message in enumerate(collected, 1):
        # Заголовок сообщения
        to_export.append(f"\n--- Сообщение #{i} ---")

        # дата
        if message.date:
            to_export.append(f"Дата: {message.date.strftime('%Y-%m-%d %H:%M:%S')}")

        # форвард?
        if message.forward_origin:
            origin = message.forward_origin

            if isinstance(origin, MessageOriginUser):
                u = origin.sender_user
                full_name = " ".join(x for x in [u.first_name, u.last_name] if x)
                username = f"@{u.username}" if u.username else ""
                line = f"Переслано от: {full_name}"
                if username:
                    line += f" ({username})"
                to_export.append(line)

            elif isinstance(origin, MessageOriginHiddenUser):
                to_export.append(f"Переслано от: {origin.sender_user_name}")

            elif isinstance(origin, MessageOriginChannel):
                chat_title = getattr(origin.chat, "title", None) or "Channel"
                to_export.append(f"Переслано от канала: {chat_title}")

            elif isinstance(origin, MessageOriginChat):
                chat_title = getattr(origin.chat, "title", None) or "Chat"
                to_export.append(f"Переслано от чата: {chat_title}")

            else:
                to_export.append("Переслано от: unknown")

        else:
            # обычное сообщение (НЕ форвард)
            if message.from_user:
                u = message.from_user
                full_name = " ".join(x for x in [u.first_name, u.last_name] if x)
                username = f"@{u.username}" if u.username else ""
                line = f"От: {full_name}"
                if username:
                    line += f" ({username})"
                to_export.append(line)

        if message.photo:
            to_export.append("[Фото]")
            if message.caption:
                to_export.append(f"Подпись: {message.caption}")

        if message.document:
            to_export.append(f"[Файл]: {message.document.file_name}")
            if message.caption:
                to_export.append(f"Подпись: {message.caption}")

        if message.video:
            to_export.append("[Видео]")
            if message.caption:
                to_export.append(f"Подпись: {message.caption}")

        if message.audio:
            to_export.append(f"[Аудио]: {message.audio.file_name}")
            if message.caption:
                to_export.append(f"Подпись: {message.caption}")

        if message.video_note:
            to_export.append("[Кружок]")

        if message.voice:
            to_export.append("[Голосовое сообщение]")

        if message.sticker:
            to_export.append(f"[Стикер]: {message.sticker.emoji}")

        if message.contact:
            to_export.append(f"[Контакт]: {message.contact.phone_number}")

        if message.checklist:
            to_export.append(f"[Список]: {message.checklist.title}")
            for ChecklistTask in message.checklist.tasks:
                to_export.append(f"  - {ChecklistTask.text}")

        if message.poll:
            poll = message.poll
            to_export.append("[Опрос]")
            to_export.append(f"Вопрос: {poll.question}")
            to_export.append("Варианты:")
            for option in poll.options:
                to_export.append(f"  - {option.text} — {option.voter_count} голосов")
            to_export.append(f"Всего голосов: {poll.total_voter_count}")

            if poll.type == "quiz":
                to_export.append("Тип: викторина")
                if poll.correct_option_id is not None:
                    correct = poll.options[poll.correct_option_id]
                    to_export.append(f"Правильный ответ: {correct.text}")
            else:
                to_export.append("Тип: обычный опрос")

            if poll.allows_multiple_answers:
                to_export.append("Несколько ответов: да")
            else:
                to_export.append("Несколько ответов: нет")

            if poll.explanation:
                to_export.append(f"Объяснение: {poll.explanation}")

        # текст сообщения
        if message.text:
            to_export.append(message.text)

    await state.clear()
    txt_text = "\n".join(to_export)
    filename = f"export{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{random.randint(0, 6767)}.txt"

    with open (f"{filename}", "w", encoding="utf-8") as f:
        f.write(f"Telegram to .txt экспорт {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{txt_text}")
    file = FSInputFile(filename)
    try:
        await callback.message.answer_document(file, caption="Экспортировано!\n\nЖелаете сделать ещё один экспорт?", reply_markup=keyboards.export_again_kb)
    except:
        await callback.message.answer("Экспорт не удался. Попробуйте экспортировать меньше сообщений.")
    finally:
        await callback.answer()
        await state.clear()
        if os.path.exists(filename):
            os.remove(filename)
