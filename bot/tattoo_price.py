from aiogram import types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

BASE_PRICE = 3000

size_coeff = {
    1: 0.8,
    2: 1.0,
    3: 1.4
}

location_coeff = {
    1: 1.0,  # плечо
    2: 1.0,  # предплечье / верхняя рука
    3: 1.3,  # спина
    4: 1.3,  # грудь / рёбра
    5: 1.1,  # нога
    6: 1.4,  # шея
    7: 1.5,  # кисть
    8: 1.6   # лицо
}

style_coeff = {
    1: 1.0,  # минимализм
    2: 1.1,  # геометрия
    3: 1.1,  # орнамент
    4: 1.2,  # традишнел
    5: 1.3,  # неотрадишнел
    6: 1.4,  # акварель
    7: 1.5,  # реализм
    8: 1.4,  # чикано
    9: 1.6   # биомеханика
}

overlap_coeff = {
    1: 1.0,  # нет перекрытия
    2: 1.3   # да, перекрытие
}

size_text = [
    "Маленькая (до ≈ 100 см²)",
    "Средняя (≈ 100 – 200 см²)",
    "Большая (от ≈ 200 см² и больше)"
]
location_text = [
    "Плечо (верхняя часть руки)",
    "Предплечье / Верхняя рука",
    "Спина (верх или поясница)",
    "Грудная клетка / Рёбра",
    "Нога (голень, бедро)",
    "Шея / Затылок",
    "Кисть / Запястье",
    "Лицо / Шея (фейс-тату)"
]
style_text = [
    "Минимализм",
    "Геометрия",
    "Орнамент",
    "Традишнел / Олдскул",
    "Неотрадишнел",
    "Акварель",
    "Реализм",
    "Чикано",
    "Биомеханика"
]
overlap_text = [
    "Нет (новая татуировка)",
    "Да (перекрытие старой)"
]

class TattooPriceFSM(StatesGroup):
    size = State()
    location = State()
    style = State()
    overlap = State()

async def start_tattoo_price(message: types.Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    for i, t in enumerate(size_text, 1):
        builder.button(text=t, callback_data=f"tattoo_size:{i}")
    builder.adjust(1)
    await message.answer("Выберите размер татуировки:", reply_markup=builder.as_markup())
    await state.set_state(TattooPriceFSM.size)

async def process_size(callback: types.CallbackQuery, state: FSMContext):
    size = int(callback.data.split(":")[1])
    await state.update_data(size=size)
    builder = InlineKeyboardBuilder()
    for i, t in enumerate(location_text, 1):
        builder.button(text=t, callback_data=f"tattoo_location:{i}")
    builder.adjust(3)
    await callback.message.edit_text("Выберите расположение татуировки:", reply_markup=builder.as_markup())
    await state.set_state(TattooPriceFSM.location)

async def process_location(callback: types.CallbackQuery, state: FSMContext):
    location = int(callback.data.split(":")[1])
    await state.update_data(location=location)
    builder = InlineKeyboardBuilder()
    for i, t in enumerate(style_text, 1):
        builder.button(text=t, callback_data=f"tattoo_style:{i}")
    builder.adjust(3)
    await callback.message.edit_text("Выберите стиль татуировки:", reply_markup=builder.as_markup())
    await state.set_state(TattooPriceFSM.style)

async def process_style(callback: types.CallbackQuery, state: FSMContext):
    style = int(callback.data.split(":")[1])
    await state.update_data(style=style)
    builder = InlineKeyboardBuilder()
    for i, t in enumerate(overlap_text, 1):
        builder.button(text=t, callback_data=f"tattoo_overlap:{i}")
    builder.adjust(2)
    await callback.message.edit_text("Требуется ли перекрытие старой татуировки?", reply_markup=builder.as_markup())
    await state.set_state(TattooPriceFSM.overlap)

async def process_overlap(callback: types.CallbackQuery, state: FSMContext):
    overlap = int(callback.data.split(":")[1])
    data = await state.get_data()
    size = data.get("size")
    location = data.get("location")
    style = data.get("style")
    price = int(BASE_PRICE * size_coeff[size] * location_coeff[location] * style_coeff[style] * overlap_coeff[overlap])
    await state.clear()
    await callback.message.edit_text(
        f"<b>Примерная стоимость татуировки:</b> <code>{price} ₽</code>\n\n"
        f"<b>Размер:</b> {size_text[size-1]}\n"
        f"<b>Расположение:</b> {location_text[location-1]}\n"
        f"<b>Стиль:</b> {style_text[style-1]}\n"
        f"<b>Перекрытие:</b> {overlap_text[overlap-1]}\n",
        parse_mode="HTML"
    ) 