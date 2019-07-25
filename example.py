from tablegen import Course, Table
import csv


def parse_course(course_code, f):
    rdr = csv.reader(f)
    courses = []

    for line in rdr:
        if line[3] in course_code:
            courses.append(Course(line[3], line[4], line[5], line[16]))

    return courses


with open("data/courses.txt", "r", encoding="UTF-8") as f:
    codes = f.read().split("\n")

with open("data/2019-2-course.csv", "r", encoding="UTF-8") as f:
    table = Table(*parse_course(codes, f))

with open("data/tables.txt", "w",encoding="UTF-8") as f:
    f.write(table.generate_tables())
