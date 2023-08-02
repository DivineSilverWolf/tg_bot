import aiogram
from DataBase import Session, User, BasicQuests, Topics, Statistic
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types, Bot
from StateUser import UserSectionsState, UserStatusState
from DataBase.patch import basic_quest_patch, extended_answer_questions, quest_file_jng, quest_solution_patch_txt, quest_solution_patch, absolute_patch
import os
from pathlib import Path
class Tasks:
    keyboard = types.ReplyKeyboardMarkup(row_width=1)

    button1 = types.KeyboardButton('Получить задание')
    button2 = types.KeyboardButton('Меню')
    # Добавляем кнопки в меню
    async def quest_type(self, message: types.Message, state: FSMContext):
        if message.text == 'Физика':
            await state.update_data(current_task =["Физика"])
            await state.set_state(UserSectionsState.TASK)
        elif message.text == 'Математика':
            await state.update_data(current_task=["Математика"])
            await state.set_state(UserSectionsState.TASK)
        await self.bot.send_message(chat_id=message.chat.id, text="--------------------------------------------------",
                               reply_markup=self.keyboard)
    async def give_task(self, message: types.Message, state: FSMContext):
        state_get_data = await state.get_data()
        chat_id = message.chat.id
        quest_solution = state_get_data['solution']
        topic_id = state_get_data['current_task']
        quest_solution_bool = None
        if quest_solution == "Задачи":
            quest_solution = basic_quest_patch
            quest_solution_bool = True
        elif quest_solution == "Задачи с развёрнутым ответом":
            quest_solution = extended_answer_questions
            quest_solution_bool = False
        if topic_id[0] == "Физика":
            topic_id = "fizic"
        elif topic_id[0] == "Математика":
            topic_id = "matematic"

        # Запрос к таблице статистики
        result = self.session.query(Statistic).join(BasicQuests).filter(
            Statistic.chat_id == chat_id,
            BasicQuests.topic == topic_id,
            BasicQuests.quest_solution == quest_solution_bool,
            Statistic.right_decision == None
        ).first()
        quest_id = None
        # Проверка на наличие результата
        if result:
            quest_id = result.get_quest_ID()
            print(f"Найденное quest_ID: {quest_id}")
        else:
            # Запрос к таблице статистики
            result = self.session.query(BasicQuests).filter(
                BasicQuests.topic == topic_id,
                BasicQuests.quest_solution == quest_solution_bool,
                BasicQuests.quest_ID.notin_(self.session.query(Statistic.quest_ID).filter(Statistic.chat_id == chat_id))
            ).first()

            # Проверка на наличие результата
            if result:
                quest_id = result.quest_ID
                print(f"Найденный quest_ID: {quest_id}")
            else:
                print("Задание с заданными параметрами не найдено")
        if quest_id is None:
            await self.bot.send_message(chat_id=chat_id, text="Вы выполнили все задания в этом разделе! Приходите завтра, мы порадуем вас новым контентом!")
        else:
            result = self.session.query(BasicQuests).filter_by(quest_ID=quest_id).first()
            assignment_number = result.get_assignment_number()
            patchQuest = os.path.join(absolute_patch, topic_id)
            patchQuest = os.path.join(patchQuest, quest_solution)
            patchQuest = os.path.join(patchQuest, assignment_number)
            files = self.filter(quest_file_jng, patchQuest)
            for i in files:
                print(i)
                await message.answer_photo(photo=types.InputFile(i))
    async def go_to_menu(self, message: types.Message, state: FSMContext):
        await state.set_state(UserSectionsState.MENU)
        await message.answer(text="Меню", reply_markup=self.keyboard1)


    def init_handlers(self):
        self.dp.register_message_handler(self.quest_type, state=[UserSectionsState.SOLUTION, UserStatusState.USER])
        self.dp.register_message_handler(self.give_task, text="Получить задание", state=[UserSectionsState.TASK, UserStatusState.USER])
        self.dp.register_message_handler(self.go_to_menu, text="Меню", state=[UserSectionsState.TASK, UserStatusState.USER])
    def filter(self, pattern, path):
        files = Path(path).rglob('задание_*.jpg')
        return files

    def __init__(self, session: Session, dp: Dispatcher, bot: Bot, keyboard1: types.ReplyKeyboardMarkup):
        self.session = session
        self.dp = dp
        self.keyboard.add(self.button1, self.button2)
        self.bot = bot
        self.init_handlers()
        self.keyboard1 = keyboard1
