# Фукции для бота

from aiogram import types
from aiogram.dispatcher import FSMContext


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
    Печатает данные пользователя 
    """
    await InItStateUser(message, state)
    
    allUserData = await state.get_data() # загружаем статусы пользователя
    userState = await state.get_state()  # загружаем состояния пользователя

    userID = str(allUserData['userID'])
    userName = str(allUserData['userName'])
    firstName = str(allUserData['firstName'])
    lastName = str(allUserData['lastName'])

    print('\nТекушие данный пользователя:')
    print('userID: ' + userID)
    print('userName: ' + userName)
    print('firstName: ' + firstName)
    print('lastName: ' + lastName)
    print('FSM: ' + userState)