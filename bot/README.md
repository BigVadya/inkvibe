# 🤖 Tattoo Studio Bot

Telegram-бот для записи клиентов в тату-студию. Реализован на [aiogram](https://docs.aiogram.dev/) с асинхронной работой с базой данных через [aiosqlite](https://github.com/omnilib/aiosqlite).

---

## 🚀 Возможности

- Регистрация пользователя (ФИО, возраст)
- Выбор мастера, даты и времени для записи
- Проверка занятости времени у мастера
- Просмотр и отмена своих записей
- История отменённых записей
- Удобное меню и навигация через inline-кнопки

---

## 🛠️ Технологии

- Python 3.11+
- [aiogram](https://docs.aiogram.dev/) — современный асинхронный Telegram Bot API
- [aiosqlite](https://github.com/omnilib/aiosqlite) — асинхронная работа с SQLite

---

## ⚡ Быстрый старт

1. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Укажите токен бота:**
   - В файле `.env` или через переменную окружения `BOT_TOKEN`.
   - Или замените переменную `API_TOKEN` в `bot.py` на свой токен.
3. **Запустите бота:**
   ```bash
   python bot.py
   ```

---

## 📂 Структура

- `bot.py` — основной код бота
- `tattoo.db` — база данных SQLite (создаётся автоматически)
- `requirements.txt` — зависимости

---

## 👤 Автор

- GitHub: [BigVadya](https://github.com/BigVadya)

---

## 📝 Лицензия

MIT
