import re
from datetime import datetime

class FileParser:
    def __init__(self, sess):
        self._session = sess

    @staticmethod
    def lessons_creator(filename):
        add_lessons = []
        with open(filename, "r") as lss:
            import task3
            for idx, ls in enumerate(lss):
                if idx <= 1:
                    continue
                ls_re = re.match(r"\s([a-z0-9-]*)\s*\|\s*([0-9]*)\s\|\s*([a-z]*)\s*\|\s([0-9-\s:\.]*)", ls)
                if ls_re:
                    ldate = ls_re.group(4).rstrip()
                    if '.' not in ldate:
                        dtt = datetime.strptime(ldate, '%Y-%m-%d %H:%M:%S')
                    else:
                        dtt = datetime.strptime(ldate, '%Y-%m-%d %H:%M:%S.%f')
                    print(ls_re.group(1), ls_re.group(2), ls_re.group(3), ldate)
                    add_lessons.append(task3.Lessons(id=ls_re.group(1), event_id=int(ls_re.group(2)), subject=ls_re.group(3), scheduled_time=dtt))

        return list(dict.fromkeys(add_lessons))

    @staticmethod
    def quality_creator(filename):
        add_quality = []
        with open(filename, "r") as qa:
            import task3
            for idx, q in enumerate(qa):
                if idx <= 1:
                    continue
                q_re = re.match(r"\s([a-z0-9-]*)\s*\|\s*([0-9])", q)
                if q_re:
                    add_quality.append(task3.Quality(lesson_id=q_re.group(1), tech_quality=int(q_re.group(2))))
        return list(dict.fromkeys(add_quality))


    @staticmethod
    def users_creator(filename):
        add_user = []
        users_dict = {}
        with open(filename, 'r') as au:
            import task3
            for idx, us in enumerate(au):
                if idx <= 1:
                    continue
                u_re = re.match(r"\s([a-z0-9-]*)\s*\|\s*([a-z]*)", us)
                if u_re:
                    if u_re.group(1) not in users_dict:
                        add_user.append(task3.Users(id=u_re.group(1), role=u_re.group(2)))
                        users_dict[u_re.group(1)] = 1 #there are repeating line in the file users.txt
        return list(dict.fromkeys(add_user))

    def participants_create(self, filename):
        add_part = []
        with open(filename, 'r') as pp:
            import task3
            for idx, p, in enumerate(pp):
                if idx <= 1:
                    continue
                p_re = re.match(r"\s*([0-9-]*)\s*\|\s*([a-z0-9-]*)", p)
                if p_re:
                    add_part.append(task3.Participants(user_id=p_re.group(2), event_id=int(p_re.group(1))))

        return list(dict.fromkeys(add_part))