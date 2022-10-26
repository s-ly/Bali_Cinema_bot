# Фукции для бота

from aiogram import types
from aiogram.dispatcher import FSMContext
import logging # модуль логирования


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
    Инициирует данные пользователя 
    """        
    await state.update_data(userID=message.chat.id)
    await state.update_data(userName=message.chat.username)
    await state.update_data(firstName=message.chat.first_name)
    await state.update_data(lastName=message.chat.last_name)
    # await state.update_data(userDanceSelect='not selected')


async def print_userStatus (message: types.Message, state: FSMContext):
    """ 
    Печатает данные пользователя на экран и в лог.
    """
    await InItStateUser(message, state)
    
    allUserData = await state.get_data() # загружаем статусы пользователя
    userState = await state.get_state()  # загружаем состояния пользователя

    userID = str(allUserData['userID'])
    userName = str(allUserData['userName'])
    firstName = str(allUserData['firstName'])
    lastName = str(allUserData['lastName'])

    logging.info('Текушие данный пользователя:')
    logging.info('userID: ' + userID)
    logging.info('userName: ' + userName)
    logging.info('firstName: ' + firstName)
    logging.info('lastName: ' + lastName)
    logging.info('FSM: ' + userState + '\n')