from aiogram import Router, F, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot_config import database

complaint_router = Router()

# FSM-состояния
class ComplaintFSM(StatesGroup):
    name = State()
    contact = State()
    complaint = State()


@complaint_router.message(F.text == "/complaint")  # Используем F.text для фильтрации
async def start_complaint(message: types.Message, state: FSMContext):
    await message.answer("Как вас зовут?")
    await state.set_state(ComplaintFSM.name)


@complaint_router.message(ComplaintFSM.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if not name:
        await message.answer("Пожалуйста, введите ваше имя.")
        return
    await state.update_data(name=name)
    await message.answer("Укажите ваш номер телефона или аккаунт в соцсетях:")
    await state.set_state(ComplaintFSM.contact)


@complaint_router.message(ComplaintFSM.contact)
async def process_contact(message: types.Message, state: FSMContext):
    contact = message.text.strip()
    if not contact:
        await message.answer("Пожалуйста, введите контактные данные.")
        return
    await state.update_data(contact=contact)
    await message.answer("Опишите вашу жалобу:")
    await state.set_state(ComplaintFSM.complaint)


@complaint_router.message(ComplaintFSM.complaint)
async def process_complaint(message: types.Message, state: FSMContext):
    complaint = message.text.strip()
    if not complaint:
        await message.answer("Пожалуйста, опишите вашу жалобу.")
        return
    await state.update_data(complaint=complaint)
    data = await state.get_data()

    # Сохранение данных в базу
    database.save_complaint(data)

    # Подтверждение
    await message.answer(
        "Ваша жалоба успешно сохранена. Спасибо за ваш отзыв!"
    )
    await state.clear()
