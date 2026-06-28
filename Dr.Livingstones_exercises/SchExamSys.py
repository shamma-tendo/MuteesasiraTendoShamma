class Learner:
    def __init__(self, name, reg_no):
        self.name   = name
        self.reg_no = reg_no

    def calculate_final_grade(self):
        raise NotImplementedError("Subclasses must implement this")


class Undergraduate(Learner):
    def __init__(self, name, reg_no, score):
        super().__init__(name, reg_no)
        self.score = score

    def calculate_final_grade(self):   # simple: score IS the grade
        return self.score


class Postgraduate(Learner):
    def __init__(self, name, reg_no, coursework, research):
        super().__init__(name, reg_no)
        self.coursework = coursework
        self.research   = research

    def calculate_final_grade(self):   # weighted average
        return (self.coursework * 0.4) + (self.research * 0.6)


# Polymorphism: same call, different calculation
learners = [
    Undergraduate("Tom", "UG01", 78),
    Postgraduate("Zara", "PG01", 80, 90),
]
for l in learners:
    print(f"{l.name}: {l.calculate_final_grade()}")