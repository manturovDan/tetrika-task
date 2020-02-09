import re
from datetime import datetime


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

    return add_lessons