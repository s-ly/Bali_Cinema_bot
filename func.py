# Фукции для бота

from aiogram import types
from aiogram.dispatcher import FSMContext
import logging

from app import name # модуль логирования


# Конфигурация логирование
# https://webdevblog.ru/logging-v-python/
# level - уровень регистрации
# filename - файл вывода
# format - дата и само сообщение
# datefmt - формат даты
file_log = logging.FileHandler('app.log')
console_out = logging.StreamHandler()
logging.basicConfig(
    level=logging.INFO, 
    handlers=(file_log, console_out), 
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M')


async def InItStateUser(message: types.Message, state: FSMContext):
    """ 
    Инициирует данные пользователя.
    Если id есть в списке, то этот пользователь админ, ему меняю статус admin на True.
    """        
    users_admin = {'Segey': '80315171'}
    await state.update_data(userID=message.chat.id)
    await state.update_data(userName=message.chat.username)
    await state.update_data(firstName=message.chat.first_name)
    await state.update_data(lastName=message.chat.last_name)
    await state.update_data(admin=False)
    await state.update_data(number_seats=None)
    await state.update_data(pay_method=None)
    await state.update_data(telegram_nick=None)
    await state.update_data(name=None)

    # Проверка на админа
    allUserData = await state.get_data() 
    userID = str(allUserData['userID'])
    for k, v in users_admin.items():
        if v == userID:
            await state.update_data(admin=True)


async def print_userStatus (message: types.Message, state: FSMContext):
    """ 
    Печатает данные пользователя на экран и в лог.
    """
    # await InItStateUser(message, state)
    
    allUserData = await state.get_data() # загружаем статусы пользователя
    userState = await state.get_state()  # загружаем состояния пользователя

    userID = str(allUserData['userID'])
    userName = str(allUserData['userName'])
    firstName = str(allUserData['firstName'])
    lastName = str(allUserData['lastName'])
    admim = str(allUserData['admin'])
    number_seats = str(allUserData['number_seats'])
    pay_method = str(allUserData['pay_method'])
    telegram_nick = str(allUserData['telegram_nick'])
    name = str(allUserData['name'])

    logging.info('Текушие данный пользователя:')
    logging.info('userID: ' + userID)
    logging.info('userName: ' + userName)
    logging.info('firstName: ' + firstName)
    logging.info('lastName: ' + lastName)
    logging.info('Admin: ' + admim)
    logging.info('number_seats: ' + number_seats)
    logging.info('pay_method: ' + pay_method)
    logging.info('telegram_nick: ' + telegram_nick)
    logging.info('name: ' + name)
    logging.info('FSM: ' + userState + '\n')