# Телеграм-бот для записи в кино Лии t.me/Bali_Cinema_bot
# Главный модуль

from aiogram import Bot                        # главная сущность бота
from aiogram import Dispatcher                 # соединяем бота и данные
from aiogram import executor                   # нужен при запуске
from aiogram import types                      # берём сообщение
from aiogram.types import InlineKeyboardMarkup # Инлайн-клавиатура
from aiogram.types import InlineKeyboardButton # Инлайн-кнопки
import tokenBots                               # мои токены
import func                                    # мой модуль с токинами

# Машина состояний
from aiogram.dispatcher.filters.state import State, StatesGroup
# хранение контекста
from aiogram.dispatcher import FSMContext
# хранения контекста в ОЗУ
from aiogram.contrib.fsm_storage.memory import MemoryStorage 


###################################################################################################
# Инициализация
###################################################################################################
# Переключение токенов
# API_TOKEN = tokenBots.workToken # рабочий бот
API_TOKEN = tokenBots.testToken # тестовый бот

# Инициируем бота
storage = MemoryStorage() # хранение контекста в ОЗУ
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

# Создаём состояния
class StateGroupFSM(StatesGroup):
    usStat_default = State()  # по умолчанию
    usStat_choiceSeats = State()  # выбор кол-ва мест
    usStat_telegramNick = State()  # идёт ввод Телеграм-ника
    usStat_name = State()  # идёт ввод имя пользователя
    usStat_paySelect = State()  # идёт выбор способа оплаты
    usStat_paySelectCompleted = State()  # выбран способ оплаты
    usStat_sendPayScreen = State()  # отправь принскрин оплаты


###################################################################################################
# Клавиатуры
###################################################################################################
inKey_viewEventDetails = InlineKeyboardMarkup()
inKey_bookTicket = InlineKeyboardMarkup()
inKey_payMethod = InlineKeyboardMarkup()

butData_viewEventDetails = [
    'Посмотреть информацию о событии', 
    'viewEventDetails']

butData_bookTicket = [
    'Забронировать билет', 
    'bookTicket']

butData_rupees = [
    'Рупий', 
    'rupees']

butData_usdt = [
    'USDT', 
    'usdt']


inBut_viewEventDetails = InlineKeyboardButton(
    text=butData_viewEventDetails[0], 
    callback_data=butData_viewEventDetails[1])
inKey_viewEventDetails.add(inBut_viewEventDetails)

inBut_bookTicket = InlineKeyboardButton(
    text=butData_bookTicket[0], 
    callback_data=butData_bookTicket[1])
inKey_bookTicket.add(inBut_bookTicket)

inBut_rupees = InlineKeyboardButton(
    text=butData_rupees[0], 
    callback_data=butData_rupees[1])
inKey_payMethod.add(inBut_rupees)

inBut_usdt = InlineKeyboardButton(
    text=butData_usdt[0], 
    callback_data=butData_usdt[1])
inKey_payMethod.add(inBut_usdt)


###################################################################################################
# Слушаем сообщения
###################################################################################################
@dp.message_handler(state=StateGroupFSM.usStat_choiceSeats)
async def choiceSeats(message: types.Message, state: FSMContext):
    """
    Отвечает на ввод кол-ва мест. 
    Записывает ответ пользователя (кол-во мест) в виде типа int.

    """ 
    # await state.update_data(number_seats=int(message.text))    
    await state.update_data(number_seats=message.text)    
    await StateGroupFSM.usStat_telegramNick.set() # Инициирует сост-е пользователя 
    await message.answer('Введите свой ник в Телеграме:.')
    await func.print_userStatus(message, state)


@dp.message_handler(state=StateGroupFSM.usStat_telegramNick)
async def telegramNick(message: types.Message, state: FSMContext):
    """
    Отвечает на ввод Телеграм-ника. 
    """    
    await StateGroupFSM.usStat_name.set() # Инициирует сост-е пользователя 
    await message.answer('Введите ваше Имя:')
    await func.print_userStatus(message, state)


@dp.message_handler(state=StateGroupFSM.usStat_name)
async def name(message: types.Message, state: FSMContext):
    """
    Отвечает на ввод Имени пользователя. 
    Вывродит кнопки выбора способа оплаты.
    """    
    await StateGroupFSM.usStat_paySelect.set() # Инициирует сост-е пользователя 
    await message.answer('Оплатить x * y. Выберите способ оплаты:', reply_markup=inKey_payMethod)
    await func.print_userStatus(message, state)


@dp.message_handler(state=StateGroupFSM.usStat_paySelectCompleted)
async def sendPayScreen(message: types.Message, state: FSMContext):
    """
    Отвечает на отправку принскрина оплаты.
    Состояние - когда выбран способ оплаты
    """    
    await StateGroupFSM.usStat_sendPayScreen.set() # Сост-е: получен скриншот 
    await message.answer('бронь ожидает')
    await func.print_userStatus(message, state)
    


@dp.message_handler(state='*')
async def all_mess(message: types.Message, state: FSMContext):
    """
    Отвечает на всё, в любом состоянии. Инициирует все данные.
    Выводит кнопку для просмотра информации о событии.
    Ещё показывает в консоль текущее состояние пользователя, 
    которое должно быть userState_default.
    """
    await func.InItStateUser(message, state) # Инициирует данные пользователя
    await StateGroupFSM.usStat_default.set() # Инициирует состояние пользователя
    await message.answer('Привет, я бот для записи в кино.', reply_markup=inKey_viewEventDetails)
    await func.print_userStatus(message, state)


###################################################################################################
# Слушаем инлайн кнопки
###################################################################################################
@dp.callback_query_handler(text=butData_viewEventDetails[1], state=StateGroupFSM.usStat_default)
async def callbackInline_inBut_viewEventDetails(
    call_inline: types.CallbackQuery, state: FSMContext):
    """
    Отвечает на инлайн-кнопку 'Показать афишу' - inBut_viewEventDetails.
    Выводит кнопку для бронирования.
    """
    await call_inline.answer('Хорошо')
    textAnswer = "Афиша"
    await call_inline.message.answer(textAnswer, reply_markup=inKey_bookTicket)
    await func.print_userStatus(call_inline.message, state)


@dp.callback_query_handler(text=butData_bookTicket[1], state=StateGroupFSM.usStat_default)
async def callbackInline_inBut_bookTicket(
    call_inline: types.CallbackQuery, state: FSMContext):
    """
    Отвечает на инлайн-кнопку 'Забронировать' - inBut_bookTicket
    """
    await StateGroupFSM.usStat_choiceSeats.set() # Инициирует сост-е пользователя 'выбор мест'
    await call_inline.answer('Хорошо')
    textAnswer = "Стоимость X, осталось Y мест. Введите кол-во мест."
    await call_inline.message.answer(textAnswer)
    await func.print_userStatus(call_inline.message, state)


@dp.callback_query_handler(text=butData_rupees[1], state=StateGroupFSM.usStat_paySelect)
async def callbackInline_inBut_rupees(
    call_inline: types.CallbackQuery, state: FSMContext):
    """
    Отвечает на инлайн-кнопку 'Рупий' - inBut_rupees
    """
    await StateGroupFSM.usStat_paySelectCompleted.set() # Инициирует сост-е 'оплата выбрана'
    await call_inline.answer('Хорошо')
    textAnswer = "Если Рупий, то платим так-то..."
    textAnswwerScreen = "Потом пришлите скрин оплаты."
    await call_inline.message.answer(textAnswer)
    await call_inline.message.answer(textAnswwerScreen)
    await func.print_userStatus(call_inline.message, state)


@dp.callback_query_handler(text=butData_usdt[1], state=StateGroupFSM.usStat_paySelect)
async def callbackInline_inBut_usdt(
    call_inline: types.CallbackQuery, state: FSMContext):
    """
    Отвечает на инлайн-кнопку 'USDT' - inBut_usdt
    """
    await StateGroupFSM.usStat_paySelectCompleted.set() # Инициирует сост-е 'оплата выбрана'
    await call_inline.answer('Хорошо')
    textAnswer = "Если USDT, то платим так-то..."
    textAnswwerScreen = "Потом пришлите скрин оплаты."
    await call_inline.message.answer(textAnswer)
    await call_inline.message.answer(textAnswwerScreen)
    await func.print_userStatus(call_inline.message, state)


###################################################################################################
# Запуск бота
###################################################################################################
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)