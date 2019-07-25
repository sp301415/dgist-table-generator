import csv
from itertools import product, combinations
from collections import defaultdict


class Course:
    def __init__(self, code):
        f = open("2019-2-course.csv", "r", encoding = "UTF-8")
        rdr = csv.reader(f)
        self.code = code
        self.time = {}
        self.title = ""
        self.class_num = []
        self.credit = 0
        for line in rdr:
            if line[3] == self.code:
                self.title = line[5]
                self.time[int(line[4])] = {i[0]: [float(j.replace(":", ".")) for j in i[1:12].split("-")]
                                           for i in line[16].split(", ")}
                self.class_num.append(int(line[4]))
                self.credit = float(line[13])
        f.close()

    def get_info(self):
        return self.code, self.title, self.class_num, self.time


class Table:
    def __init__(self, *courses):
        self.courses = courses

    def get_credits(self):
        return sum(course.credit for course in self.courses)

    @staticmethod
    def check_overlap(time1, time2):
        for day in "월화수목금":
            try:
                # sort time1 and time2
                if time1[day][1] > time2[day][1]:
                    time1, time2 = time2, time1
                if time1[day][1] > time2[day][0]:
                    return True
            except KeyError:
                continue
        return False

    @staticmethod
    def merge_by_day(courses):
        # merge time data by day
        # used for final generate_tables
        # result looks like: {day: [{course: time}, ...], ...}

        table_day = defaultdict(list)

        for course, time in courses.items():
            for day, hour in time.items():
                table_day[day].append({course: hour})

        return dict(table_day)

    def check_courses(self, dict_course):
        # choose any two courses and check whether it overlaps or not
        for i in combinations(dict_course.values(), 2):
            if self.check_overlap(*i):
                return False
        return True

    def generate_tables(self):
        # Generate all possible permutations of class number...
        possible_tables_num = list(product(*[course.class_num for course in self.courses]))
        # ...and use it to construct all possible time tables.
        # TODO: somehow include class number information here, or at least simplify the algorithm.
        possible_tables = [{self.courses[j]: self.courses[j].time[k] for j, k in enumerate(i)}
                           for i in possible_tables_num]

        tables = [self.merge_by_day(t) for t in possible_tables if self.check_courses(t)]

        string = ""
        for num, table in enumerate(tables):
            string += f"Table {num + 1}\n"
            for day in "월화수목금":
                try:
                    string += f"{day}: "
                    # Since data structure is very complicated, this ugly code happens!
                    # TODO: simply data structure.
                    table[day].sort(key=lambda x: list(x.values())[0][0])
                    for data in table[day]:
                        for course, time in data.items():
                            string += f"{course.title}: {'-'.join(str(i) + '0' for i in time).replace('.', ':')} "
                    string += "\n"
                except KeyError:
                    string += "None\n"
            string += f"학점: {self.get_credits()} \n\n"

        return string


courses = []

with open("courses.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        courses.append(Course(line.rstrip("\n")))

table = Table(*courses)

with open("tables.txt", "w") as f:
    f.write(table.generate_tables())

print("Table Generated.")
