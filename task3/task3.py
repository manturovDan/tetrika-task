import sys

from sqlalchemy import create_engine, Table, Column, Integer, String, SmallInteger, MetaData, ForeignKey, DateTime, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import FileParse


engine = create_engine('postgres+psycopg2://dbu:123@localhost:5432/dbb', echo=True)
Base = declarative_base()


class Lessons(Base):
    __tablename__ = 'lessons'

    id = Column(String, primary_key=True)
    event_id = Column(Integer)
    subject = Column(String)
    scheduled_time = Column(DateTime)

    qualities = relationship('Quality', backref='lessons')


class Participants(Base):
    __tablename__ = 'participants'

    part_id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    event_id = Column(Integer)


class Users(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    role = Column(String)

class Quality(Base):
    __tablename__ = "quality"

    id = Column(Integer, primary_key=True)
    lesson_id = Column(String, ForeignKey('lessons.id'))
    tech_quality = Column(SmallInteger)


need_init = False
if not engine.dialect.has_table(engine, 'lessons'):
    need_init = True

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

fp = FileParse.FileParser(session)

if need_init:
    session.add_all(fp.lessons_creator(sys.argv[1]))
    session.add_all(fp.quality_creator(sys.argv[2]))
    session.add_all(fp.users_creator(sys.argv[3]))
    session.add_all(fp.participants_create(sys.argv[4]))
    session.commit()
