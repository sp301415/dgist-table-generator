class Course:
    def __init__(self, code, num, title, time):
        self.code = code
        self.num = int(num)
        self.title = title
        self.time = {i[0]: i[1:12] for i in time.split(", ")}

    def get_info(self):
        return self.code, self.num, self.title, self.time
