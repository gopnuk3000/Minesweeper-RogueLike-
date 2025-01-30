class QuizMine:
    def __init__(self, quizes):
        self.quizes = quizes

    def used(self, question, answer):
        if self.quizes[question] == answer:
            return True
        else:
            return False