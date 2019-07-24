import csv
from itertools import product, combinations
from collections import defaultdict


class Course:
    def __init__(self, code):
        f = open("2019-2-course.csv", "r")
        rdr = csv.reader(f)
        self.code = code
        self.time = {}
        self.credit = 0
        self.title = ""
        self.class_num = []
        for line in rdr:
            if line[3] == self.code:
                self.title = line[5]
                self.credit = line[13]
                self.time[int(line[4])] = {i[0]: [float(j.replace(":", ".")) for j in i[1:12].split("-")] \
                                           for i in line[16].split(", ")}
                self.class_num.append(int(line[4]))
        f.close()

    def get_info(self):
        return self.code, self.title, self.class_num, self.time


class Table:
    def __init__(self, *courses):
        self.courses = courses

    @staticmethod
    def check_overlap(time1, time2):
        for day in "월화수목금":
            try:
                if ((time1[day][1] < time2[day][0])
                        or (time1[day][0] < time2[day][1])):
                    return True
            except KeyError:
                continue
        return False

    @staticmethod
    def merge_by_day(courses):
        # used for final generate_tables
        # looks like: {course object: {day: time}}, ...}

        table_day = defaultdict(list)

        for course, time in courses.items():
            for day, hour in time.items():
                table_day[day].append({course: hour})

        #"-".join(str(i) + "0" for i in hour).replace(".", ":")
        return dict(table_day)

    def check_courses(self, dict_course):
        for i in combinations(dict_course.values(), 2):
            if self.check_overlap(*i):
                return False
        return True

    def generate_tables(self):
        possible_tables_num = list(product(*[i.class_num for i in self.courses]))
        possible_tables = [{self.courses[j]: self.courses[j].time[k] for j, k in enumerate(i)}
                           for i in possible_tables_num]

        tables = [self.merge_by_day(i) for i in possible_tables if self.check_courses(i)]

        string = ""
        for p, table in enumerate(tables):
            string += f"Table {p+1}\n"
            for day in "월화수목금":
                try:
                    string += f"{day}: "
                    table[day].sort(key=lambda x: list(x.values())[0][0])
                    for i in table[day]:
                        for course, time in i.items():
                            string += f"{course.title}: {'-'.join(str(i) + '0' for i in time).replace('.', ':')} "
                    string += "\n"
                except KeyError:
                    string += "None\n"
            string += "\n"

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
