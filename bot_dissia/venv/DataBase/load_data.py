if __name__ == '__main__':
    from DataBase.models import getSession, User, Topics, BasicQuests, Session
    from patch import absolute_patch, basic_quest_patch, extended_answer_questions
    import os


    # Если нету записи добавляею в базу данных
    def check_and_add_topic(topic_name: str, session: Session):
        topic = session.query(Topics).filter_by(topic=topic_name).first()
        if topic is None:
            new_topic = Topics(topic=topic_name)
            session.add(new_topic)
            session.commit()
            print("Тема добавлена")
        else:
            print("Тема уже существует")

    def check_and_add_quest(topic_name: str, assignment_number: str, quest_solution: bool, session: Session):
        quest = session.query(BasicQuests).filter_by(topic=topic_name, quest_solution=quest_solution, assignment_number=assignment_number).first()
        if quest is None:
            new_quest = BasicQuests(topic=topic_name, assignment_number=assignment_number, quest_solution=quest_solution)
            session.add(new_quest)
            session.commit()
            print("Задание добавлено")
        else:
            print("Задание уже есть")



    db = getSession()
    # Получить список папок
    folder_list = [name for name in os.listdir(absolute_patch) if os.path.isdir(os.path.join(absolute_patch, name))]

    # Прохожусь по всем папкам из директории и исполняю функцию проверки наличия записи в бд.
    for folder in folder_list:
        check_and_add_topic(folder, db)
        print(folder)

    # Прохожусь по всем папкам из директории, захожу в каждую из них и заполняю базу количеством заданий
    for folder in folder_list:
        new_patch = os.path.join(absolute_patch, folder)
        new_patch_quest = os.path.join(new_patch, basic_quest_patch)
        new_folder_list = [name for name in os.listdir(new_patch_quest) if os.path.isdir(os.path.join(new_patch_quest, name))]
        for folder_quest in new_folder_list:
            check_and_add_quest(folder, folder_quest, True, db)
            print(folder_quest, basic_quest_patch, folder)
        new_patch_quest = os.path.join(new_patch, extended_answer_questions)
        new_folder_list = [name for name in os.listdir(new_patch_quest) if os.path.isdir(os.path.join(new_patch_quest, name))]
        for folder_quest in new_folder_list:
            check_and_add_quest(folder, folder_quest, False, db)
            print(folder_quest, extended_answer_questions, folder)