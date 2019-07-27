from itertools import product, combinations
from collections import defaultdict


class Tables:
    def __init__(self, *courses):
        self.courses = []
        for t in {c.title for c in courses}:
            self.courses.append([c for c in courses if c.title == t])

        all_tables = product(*self.courses)
        self.possible_tables = [self.arrange_table_by_day(t) for t in all_tables if self.check_courses(t)]
        if len(self.possible_tables) == 0:
            raise ValueError

        self.courses_merged = [c[0] for c in self.courses]
        self.credits = sum(c.credit for c in self.courses_merged)

    @staticmethod
    def check_overlap(c_time1, c_time2):
        for day in "월화수목금":
            try:
                time1 = [float(i) for i in c_time1[day].replace(":", ".").split("-")]
                time2 = [float(i) for i in c_time2[day].replace(":", ".").split("-")]
                # sort time1 and time2
                if time1[1] > time2[1]:
                    time1, time2 = time2, time1
                if time1[1] > time2[0]:
                    return True
            except KeyError:
                continue
        return False

    @staticmethod
    def arrange_table_by_day(table):
        # rearrange tables by day
        table_day = defaultdict(list)

        for course in table:
            for day, hour in course.time.items():
                table_day[day].append(course)

        for day in "월화수목금":
            try:
                table_day[day].sort(key=lambda x: int(x.time[day][:2]))  # sort by hour
            except KeyError:
                continue

        return dict(table_day)

    @classmethod
    def check_courses(cls, courses):
        # choose any two courses and check whether it overlaps or not
        for i in combinations([c.time for c in courses], 2):
            if cls.check_overlap(*i):
                return False
        return True

    def generate_tables(self):
        # format table to string
        formatted_tables = f"""
신청한 과목: {", ".join(c.title for c in self.courses_merged)}
총 학점 수: {self.credits}
-----------------------

"""
        for num, table in enumerate(self.possible_tables):
            formatted_tables += f"Table {num + 1} (총 학점: {self.credits})\n"
            for day in "월화수목금":
                try:
                    formatted_tables += f"{day}: "
                    for course in table[day]:
                        formatted_tables += f"\n{course.time[day]} - {course.title} ({course.num}분반)"
                    formatted_tables += "\n"
                except KeyError:
                    formatted_tables += "None\n"
            formatted_tables += f"\n\n"
        return formatted_tables
