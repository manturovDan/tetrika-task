from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('postgres+psycopg2://dbu:123@localhost:5432/dbb', echo=True)
Base = declarative_base()


class Lessons(Base):
    __tablename__ = 'lessons'

    id = Column(String, primary_key=True)
    event_id = Column(Integer)
    subject = Column(String)
    scheduled_time = Column(DateTime)

    qualities = relationship("Quality")


class Participants(Base):
    __tablename__ = 'participants'

    part_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    event_id = Column(Integer)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    role = Column(String)

class Quality(Base):
    __tablename__ = "quality"

    id = Column(Integer, primary_key=True)
    lesson_id = Column(String, ForeignKey('lessons.id'))




Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
