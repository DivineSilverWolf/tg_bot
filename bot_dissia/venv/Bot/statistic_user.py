from DataBase import User, Topics, BasicQuests, Statistic, Session
def get_statistic_user(chat_id, session: Session):
    user_statistic_solution_true = {}
    user_statistic_solution_false = {}
    user = session.query(User).filter(User.chat_id == chat_id).first()

    # Получаем все задания пользователя
    user_quests = session.query(Statistic).join(BasicQuests).filter(Statistic.chat_id == chat_id).all()

    for quest in user_quests:
        topic = session.query(BasicQuests).filter(BasicQuests.quest_ID == quest.quest_ID).first().topic
        quest_solution = session.query(BasicQuests).filter(
            BasicQuests.quest_ID == quest.quest_ID).first().quest_solution
        right_decision = session.query(Statistic).filter(
            Statistic.quest_ID == quest.quest_ID & Statistic.chat_id == quest.chat_id).first().right_decision
        if topic not in user_statistic_solution_true:
            user_statistic_solution_true[topic] = {
                'right_decisions_true': 0,
                'right_decisions_false': 0
            }
        if topic not in user_statistic_solution_false:
            user_statistic_solution_false[topic] = {
                'right_decisions_true': 0,
                'right_decisions_false': 0
            }
        if right_decision:
            if quest_solution:
                user_statistic_solution_true[topic]['right_decisions_true'] += 1
            else:
                user_statistic_solution_false[topic]['right_decisions_true'] += 1
        else:
            if quest_solution:
                user_statistic_solution_true[topic]['right_decisions_false'] += 1
            else:
                user_statistic_solution_false[topic]['right_decisions_false'] += 1

    # Выводим статистику в консоль
    print("Содержимое user_statistic_solution_true:")
    for topic, data in user_statistic_solution_true.items():
        print(f"Тема: {topic}")
        print(f"Правильные решения (true): {data['right_decisions_true']}")
        print(f"Правильные решения (false): {data['right_decisions_false']}")
    print("Содержимое user_statistic_solution_false:")
    for topic, data in user_statistic_solution_false.items():
        print(f"Тема: {topic}")
        print(f"Правильные решения (true): {data['right_decisions_true']}")
        print(f"Правильные решения (false): {data['right_decisions_false']}")