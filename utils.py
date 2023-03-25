import enum
import random
import time


class stringPlus:
    def __init__(self, string):
        self.string = string
        self.info = []

        counter_row = 0
        counter_column = 0
        for ch in self.string + '\n':
            if ch != '\n':
                counter_row += 1
            else:
                counter_column += 1
                self.info.append((counter_column, counter_row))
                counter_row = 0

    def __str__(self):
        return self.string

    def __len__(self):
        return len(self.string)

    def reformat_index(self, index):
        if index > self.info[0][1]:
            formated_index = index - self.info[0][1]
        else:
            return self.info[0][0], index

        for i in range(1, len(self.info)):
            if formated_index > self.info[i][1]:
                formated_index = index - self.info[i][1]
            else:
                return (self.info[i][0], formated_index)


class pseudoPointer:
    def __init__(self, var=None):
        self.value = [var]

    def __len__(self):
        try:
            return len(self.value[0]) - self.value[0].count('\n')
        except TypeError:
            return 1

    def set_value(self, value):
        self.value = [value]

    def get_value(self):
        return self.value[0]


class AvailableTexts(enum.Enum):
    text1 = "text1"
    text2 = "text2"
    text3 = "text3"
    text4 = "text4"


def _choose_text():
    return random.choice(list(AvailableTexts)).value


def compare_strings(str1, str2):
    mistakes = set()
    if str1 == str2:
        return mistakes
    if len(str2) > len(str1):
        length = len(str1)
    else:
        length = len(str2)

    for i in range(length):
        if str1[i] != str2[i]:
            mistakes.add(i)
    return mistakes


def count_mistakes(str1, str2):
    mistakes = 0
    if str1 == str2:
        return True
    if len(str2) > len(str1):
        lenght = len(str1)
        mistakes += (len(str2) - len(str1))
    else:
        lenght = len(str2)

    for i in range(lenght):
        if str1[i] != str2[i]:
            mistakes += 1
    return mistakes


class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = 0
        self.started = 0

    def start(self):
        self.start_time = time.monotonic()
        self.started = 1

    def reset(self):
        self.start_time = 0
        self.started = 0

    def update(self):
        if time.monotonic() - self.start_time >= self.duration:
            return self.duration
        return time.monotonic() - self.start_time

