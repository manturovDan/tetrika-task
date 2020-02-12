import sys
from datetime import timedelta
import json

from sqlalchemy import create_engine, Table, Column, Integer, String, SmallInteger, MetaData, ForeignKey, DateTime, event, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import FileParse


engine = create_engine('postgres+psycopg2://dbu:123@localhost:5432/dbb', echo=False)
Base = declarative_base()


class Lessons(Base):
    __tablename__ = 'lessons'

    id = Column(String, primary_key=True)
    event_id = Column(Integer)
    subject = Column(String)
    scheduled_time = Column(DateTime)

    qualities = relationship('Quality', backref='lessons')
    participants = relationship('Participants', backref='lessons')


class Participants(Base):
    __tablename__ = 'participants'

    part_id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), ForeignKey('users.id'))
    event_id = Column(Integer, ForeignKey('lessons.event_id'))

    user = relationship('Users', backref='participants')


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

fp = FileParse.FileParser()

if need_init:
    #check unique correctness
    session.add_all(fp.lessons_create(sys.argv[1]))
    session.add_all(fp.quality_create(sys.argv[2]))
    session.add_all(fp.users_create(sys.argv[3]))
    session.commit()
    session.add_all(fp.participants_create(sys.argv[4]))
    session.commit()

phys_lessons = session.query(Lessons).join(Quality).join(Participants).filter(and_(and_(and_(Lessons.subject == 'phys',
                                    Lessons.id == Quality.lesson_id), Lessons.event_id == Participants.event_id))).all()


stat = {}
stat_ex = {}
i = 1
for phys_les in phys_lessons:
    print(str(i) + ')')
    i += 1

    mos_date = (phys_les.scheduled_time.date() + timedelta(hours=3)).strftime("%Y-%m-%d")
    if mos_date not in stat:
        stat[mos_date] = {}
        stat_ex[mos_date] = {}
    print(phys_les.id, phys_les.event_id, phys_les.subject, mos_date)

    print('Prts:')
    for p in phys_les.participants:
        print(p.user_id, p.event_id, p.user.role)
        if p.user.role == 'tutor':
            if p.user_id not in stat[mos_date]:
                stat[mos_date][p.user_id] = {phys_les.id: []}
                stat_ex[mos_date][p.user_id] = {'lessons': 1, 'sum': 0, 'avg': 0}
            else:
                stat[mos_date][p.user_id][phys_les.id] = []
                stat_ex[mos_date][p.user_id]['lessons'] += 1

            for q in phys_les.qualities:
                stat[mos_date][p.user_id][phys_les.id].append(q.tech_quality)
                stat_ex[mos_date][p.user_id]['sum'] += 0 if q.tech_quality is None else q.tech_quality

    print('Qua:')
    for q in phys_les.qualities:
        print(q.tech_quality)

    print('\n')

resl = []

for i_date in stat_ex:
    resl.append([i_date, None, None])
    minv = -1
    for i_tut in stat_ex[i_date]:
        avg = stat_ex[i_date][i_tut]['sum'] / stat_ex[i_date][i_tut]['lessons']
        stat_ex[i_date][i_tut]['avg'] = avg

        if minv < 0 or avg < minv and avg != 0:
            minv = avg
            resl[-1][1] = i_tut
            resl[-1][2] = avg

print(json.dumps(stat))
print(json.dumps(stat_ex))
print(json.dumps(resl))

print("\nAnswer:")
for i in resl:
    print(i[0] + ' ' + i[1] + ' ' + str(i[2]))
