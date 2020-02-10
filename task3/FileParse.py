import re
from datetime import datetime

class FileParser:
    lessons_exp = re.compile(r"\s([a-z0-9-]*)\s*\|\s*([0-9]*)\s\|\s*([a-z]*)\s*\|\s([0-9-\s:\.]*)")
    quality_exp = re.compile(r"\s([a-z0-9-]*)\s*\|\s*([0-9])")
    users_exp = re.compile(r"\s([a-z0-9-]*)\s*\|\s*([a-z]*)")
    participants_exp = re.compile(r"\s*([0-9-]*)\s*\|\s*([a-z0-9-]*)")

    def regex_creator(self, filename, type_cr):
        add = []
        users_dict = {}
        with open(filename, "r") as opf:
            import task3
            for idx, i in enumerate(opf):
                if idx <= 1:
                    continue

                if type_cr == 0: #lessons
                    ls_re = re.match(self.lessons_exp, i)
                    if ls_re:
                        ldate = ls_re.group(4).rstrip()
                        if '.' not in ldate:
                            dtt = datetime.strptime(ldate, '%Y-%m-%d %H:%M:%S')
                        else:
                            dtt = datetime.strptime(ldate, '%Y-%m-%d %H:%M:%S.%f')
                        print(ls_re.group(1), ls_re.group(2), ls_re.group(3), ldate)
                        add.append(
                            task3.Lessons(id=ls_re.group(1), event_id=int(ls_re.group(2)), subject=ls_re.group(3),
                                          scheduled_time=dtt))

                elif type_cr == 1: #quality
                    q_re = re.match(self.quality_exp, i)
                    if q_re:
                        add.append(task3.Quality(lesson_id=q_re.group(1), tech_quality=int(q_re.group(2))))

                elif type_cr == 2: #users
                    u_re = re.match(self.users_exp, i)
                    if u_re:
                        if u_re.group(1) not in users_dict:
                            add.append(task3.Users(id=u_re.group(1), role=u_re.group(2)))
                            users_dict[u_re.group(1)] = 1  # there are repeating line in the file users.txt

                else:
                    p_re = re.match(self.participants_exp, i)
                    if p_re:
                        add.append(task3.Participants(user_id=p_re.group(2), event_id=int(p_re.group(1))))

        return list(dict.fromkeys(add))

    def lessons_create(self, filename):
        return self.regex_creator(filename, 0)

    def quality_create(self, filename):
        return self.regex_creator(filename, 1)

    def users_create(self, filename):
        return self.regex_creator(filename, 2)

    def participants_create(self, filename):
        return self.regex_creator(filename, 3)
