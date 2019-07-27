class Course:
    def __init__(self, code, num, title, time, credit):
        self.code = code
        self.num = num
        self.title = title
        self.time = {i[0]: i[1:12] for i in time.split(", ")}
        self.credit = float(credit)

    def get_info(self):
        return self.code, self.num, self.title, self.time, self.credit
