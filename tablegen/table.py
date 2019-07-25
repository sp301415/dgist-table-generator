from itertools import product, combinations
from collections import defaultdict


class Table:
    def __init__(self, *courses):
        self.courses = []
        for t in {c.title for c in courses}:
            self.courses.append([course for course in courses if course.title == t])

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
    def format_table(table):
        # reformat tables by day
        table_day = defaultdict(list)

        for course in table:
            for day, hour in course.time.items():
                table_day[day].append(course)

        for day in "월화수목금":
            try:
                table_day[day].sort(key=lambda x: int(x.time[day][:2])) # sort by hour
            except KeyError:
                continue

        return dict(table_day)

    def check_courses(self, courses):
        # choose any two courses and check whether it overlaps or not
        for i in combinations([c.time for c in courses], 2):
            if self.check_overlap(*i):
                return False
        return True

    def generate_tables(self):
        # Generate all possible permutations of class number...
        possible_tables = list(product(*self.courses))
        tables = [self.format_table(table) for table in possible_tables if self.check_courses(table)]

        string = ""
        for num, table in enumerate(tables):
            string += f"Table {num + 1}\n"
            for day in "월화수목금":
                try:
                    string += f"{day}: "
                    for course in table[day]:
                        string += f"\n{course.time[day]} - {course.title} ({course.num})"
                    string += "\n"
                except KeyError:
                    string += "None\n"
            string += "\n"
        return string
