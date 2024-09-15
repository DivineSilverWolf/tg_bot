# This is a sample Python script.
import aiogram
from auth_data import token
from DataBase import User, getSession, Topics, BasicQuests, Statistic
from StateUser import UserSectionsState, UserStatusState
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types# Press Shift+F10 to execute it or replace it with your code.
from aiogram.contrib.fsm_storage.memory import MemoryStorage# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State#orm django
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#redis
from Bot.statistic_user import get_statistic_user
from solve_problems import Tasks
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
def tg_bot(token):
    # Создаем массив кнопок
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton('Задачи')
    button2 = types.KeyboardButton('Задачи с развёрнутым ответом')
    button3 = types.KeyboardButton('Статистика')
    # Добавляем кнопки в меню
    keyboard.add(button1, button2, button3)

    keyboard1 = types.ReplyKeyboardMarkup(row_width=1)

    button4 = types.KeyboardButton('Физика')
    button5 = types.KeyboardButton('Математика')
    keyboard1.add(button4, button5)

    bot = Bot(token)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    session = getSession()
#    @dp.register_message_handler()
    @dp.message_handler(commands=["start"])
    async def start_message(message: types.Message, state: FSMContext):
        task = Tasks(session, dp, bot, keyboard)
        user = session.query(User).filter_by(chat_id=message.chat.id).first()
        if user is None:
            user = User(message.chat.id, message.from_user.username)
            session.add(user)
            session.commit()

        if message.chat.username == 'DissiaV23':
            await state.set_state(UserStatusState.ADMIN)
            await bot.send_message(text=f"Добро пожаловать администратор, DissiaV23!")
        else:
            await state.set_state(UserStatusState.USER)
        await state.set_state(UserSectionsState.MENU)
        await bot.send_message(chat_id=message.chat.id,
                         text='Добро пожаловать!',
                         reply_markup=keyboard)
    @dp.message_handler(state=[UserSectionsState.MENU, UserStatusState.USER])
    async def menu_message(message: types.Message, state: FSMContext):
        if message.text == 'Задачи':
            await bot.send_message(chat_id=message.chat.id, text='Вы выбрали обычные задачи')
            await bot.send_message(chat_id=message.chat.id,
                                   text='Выберите предмет',
                                   reply_markup=keyboard1)

            await state.set_state(UserSectionsState.SOLUTION)
            await state.update_data(solution="Задачи")
        elif message.text == 'Задачи с развёрнутым ответом':
            await bot.send_message(chat_id=message.chat.id, text='Вы выбрали задачи с развёрнутым ответом')
            await bot.send_message(chat_id=message.chat.id,
                                   text='Выберите предмет',
                                   reply_markup=keyboard1)
            await state.set_state(UserSectionsState.SOLUTION)
            await state.update_data(solution="Задачи с развёрнутым ответом")
        elif message.text == 'Статистика':
            await bot.send_message(chat_id=message.chat.id, text='Ваша статистика:')
            get_statistic_user(message.chat.id, session)


    @dp.message_handler(state=UserSectionsState.MENU)
    async def quest_message(message):
        print()
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    tg_bot(token)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/