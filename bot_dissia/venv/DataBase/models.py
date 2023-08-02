import sqlalchemy as db
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import ForeignKey
from os import path
Base = declarative_base()




class Topics(Base):
    __tablename__ = "Темы"

    topic = Column(String, primary_key=True)

    def __init__(self, topic: str):
        self.topic = topic
    def get_topic(self):
        return self.topic


class BasicQuests(Base):
    __tablename__ = "Задания"

    quest_ID = Column(Integer, primary_key=True)
    assignment_number = Column(String)
    topic = Column(String, ForeignKey('Темы.topic'))
    quest_solution = Column(Boolean)
    def __init__(self, assignment_number: str, topic: str, quest_solution: bool):
        self.assignment_number = assignment_number
        self.topic = topic
        self.quest_solution = quest_solution
    __table_args__ = (
        db.UniqueConstraint('assignment_number', 'topic', 'quest_solution', name='_assignment_topic_quest_uc'),
    )

    def get_id(self):
        return self.ID

    def get_assignment_number(self):
        return self.assignment_number

    def get_topic(self):
        return self.topic

    def get_quest_solution(self):
        return self.quest_solution


class User(Base):
    __tablename__ = "users"

    chat_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)

    def __init__(self, chat_id: int, username: str):
        self.chat_id = chat_id
        self.username = username
    def get_chat_id(self):
        return self.chat_id

    def get_username(self):
        return self.username



class Statistic(Base):
    __tablename__ = "statistic"
    chat_id = Column(Integer, ForeignKey('users.chat_id'), primary_key=True)
    quest_ID = Column(Integer, ForeignKey('Задания.quest_ID'), primary_key=True)
    right_decision = Column(Boolean, nullable=True)

    def __init__(self, chat_id: int, quest_ID: int, right_decision: bool):
        self.chat_id = chat_id
        self.quest_ID = quest_ID
        self.right_decision = right_decision
    def get_chat_id(self):
        return self.chat_id

    def get_quest_ID(self):
        return self.quest_ID

    def get_right_decision(self):
        return self.right_decision

def getSession() -> Session:
    # Создание всех таблиц в базе данных
    #engine = create_engine('sqlite:///DataBase/main.sqlite', echo=True)
    #if not path.exists("main.sqlite"):
    #    Base.metadata.create_all(engine)
    engine = create_engine('postgresql://postgres:admin@localhost:4444/mydatabase')
    #
    if 'user' not in Base.metadata.tables:
        Base.metadata.create_all(engine)

    # Создание сессии для работы с базой данных
    Session = sessionmaker(bind=engine)
    # session_factory = sessionmaker()
    # session_factory.configure(bind=engine)
    session = Session()
    return session