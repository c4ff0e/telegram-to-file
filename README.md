># Telegram to file 🗨️->🗒️
## [RU](#RU) | [EN](#EN)
### RU
Бот для экспорта Telegram сообщений в файл.

@tgtofile_bot - уже рабочий бот. Он [**НЕ СОХРАНЯЕТ**](https://github.com/c4ff0e/telegram-to-file/blob/main/md_helper.py#L176) ваши сообщения на сервере. Если вы всё равно боитесь за ваши данные - ниже есть [инструкция по запуску](#запуск).
- **Зачем?**  
Один раз мне понадобилось экспортировать сообщения из телеги в читаемом текстовом виде (а не html, скриншотом, или ctrl+c ctrl+v в блокнот). И я не хотел скачивать какие-то левые инструменты. А ещё потому что я могу.

- **Как?**  
Очень просто.

## Функции

- Экспорт сообщений в формат `.md`
- Экспорт сообщений в формат `.txt`
- Сохранение метаданных (дата, автор, источник пересылки)

## Запуск
### Готовый .exe
1. Скачайте [последнюю версию лаунчера](https://github.com/c4ff0e/telegram-to-file/releases/latest)
2. Запустите .exe
3. Вставьте свой токен в поле ввода ([**ПОЛУЧИТЬ ТОКЕН ЗДЕСЬ**](https://t.me/botfather))
4. Нажмите на кнопку "Start"
5. ВСЁ!   
Напишите /start в своём боте и экспортируйте свои сообщения.

### Из терминала

1. Клонируйте репозиторий:
```bash
git clone https://github.com/c4ff0e/telegram-to-file

cd telegram-to-file
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv .venv

.venv\Scripts\activate  # Windows

source .venv/bin/activate # Linux/Mac
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корне проекта с вашим токеном:
```
BOT_TOKEN=123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ
```
[**ПОЛУЧИТЬ ТОКЕН ЗДЕСЬ**](https://t.me/botfather)

5. Запустите GUI или бота напрямую:
```bash
python gui.py # GUI
python bot_main.py # Бот
```


## EN
### English

A bot for exporting Telegram messages to file.  
@tgtofile_bot - already a working bot. It [**DOES NOT SAVE**](https://github.com/c4ff0e/telegram-to-file/blob/main/md_helper.py#L176) your messages anywhere. If you're still concerned about your data privacy - see the [launch instructions](#launch) below.

- **Why?**

Once I needed to export messages from Telegram in a readable text format (not HTML, screenshots, or manual copy-paste). I didn't want to use any sketchy tools. Plus, I could build it myself.

- **How?**

Very simple.

## Features

- Export messages to `.md` format
- Export messages to `.txt` format
- Save metadata (date, author, forwarding source)

## Launch

### Pre-built .exe

1. Download the [latest launcher version](https://github.com/c4ff0e/telegram-to-file/releases/latest)
2. Run the .exe
3. Enter your bot token ([**GET TOKEN HERE**](https://t.me/botfather))
4. Click the "Start" button
5. Done!

Send /start to your bot and start exporting your messages.

### From terminal

1. Clone the repository:
```bash
git clone https://github.com/c4ff0e/telegram-to-file

cd telegram-to-file
```

2. Create and activate virtual environment:
```bash
python -m venv .venv

.venv\Scripts\activate  # Windows

source .venv/bin/activate # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file in the root directory with your token:
```
BOT_TOKEN=123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ
```
[**GET TOKEN HERE**](https://t.me/botfather)

5. Run GUI or bot directly:
```bash
python gui.py # GUI
python bot_main.py # Bot
```
