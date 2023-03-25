from utils import stringPlus, _choose_text, compare_strings


class SpeedTypingInternals:
    def __init__(self, text_to_contest=_choose_text(), test_duration=60):
        file = open("texts/" + text_to_contest + ".txt", 'r')
        self.text = stringPlus(file.read())
        self.duration = test_duration
        self.timer_value = 0
        self.mistakes_indexes = set()
        self.typos = 0

    def count_typos(self, new_mistakes):
        diff = new_mistakes - self.mistakes_indexes
        self.typos += len(diff)

    def speed_typing_check(self, typed_text):
        if self.text.string == typed_text or self.timer_value >= self.duration:
            return 1
        new_mistakes = compare_strings(self.text.string, typed_text)
        self.count_typos(new_mistakes)
        self.mistakes_indexes = new_mistakes
        return 0

    def get_mistakes_indexes(self):
        return self.mistakes_indexes

    def get_typos(self):
        return self.typos

    def set_time(self, time):
        self.timer_value = time