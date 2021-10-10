# This is a sample Python script.
import tkinter
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import tkinter as tk
import tkinter.scrolledtext as st
from textwrap import wrap
import time
import enum
import random
from tkinter import scrolledtext


class AvailableTexts(enum.Enum):
    text1 = "text1"
    text2 = "text2"
    text3 = "text3"
    text4 = "text4"


def _choose_text():
    return random.choice(list(AvailableTexts)).value


def compare_strings(str1, str2, start, stop):
    # mistakes = []
    # if str1 == str2:
    #     return 1
    # for i in range(start, stop):
    #     if str1[i] != str2[i]:
    #         mistakes.append(i)
    # return ((mistakes, 1)[len(mistakes) == 0])
    pass


class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = 0

    def start(self):
        self.start_time = time.monotonic()

    def count(self):
        if time.monotonic() - self.start_time >= self.duration:
            return 1
        return 0


class SpeedTypingInternals:
    def __init__(self, text_to_contest=_choose_text(), test_duration=60):
        file = open("texts/" + text_to_contest + ".txt", 'r')
        self.text = file.read()
        self.duration = test_duration
        self.mistakes_indexes = []

    def speed_typing_check(self, typed_text, start, stop):
        pass


class SpeedTypingInterface:
    @staticmethod
    def highlight_text(txtwidget, tag_name, lineno, start_char, end_char, bg_color=None, fg_color=None):
        txtwidget.tag_add(tag_name, f'{lineno}.{start_char}', f'{lineno}.{end_char}')
        txtwidget.tag_config(tag_name, background=bg_color, foreground=fg_color)

    def timer(self):
        pass

    def text_example(self, window, text_to_show):
        text_sample = tk.Text(window, width=50)
        text_sample.insert('0.0', text_to_show)
        text_sample.grid(column=0, row=0, columnspan=5, padx=50, pady=50)
        text_sample.config(state=tk.DISABLED, font=("Arial", 14))
        text_sample.tag_add("test", '1.0', '1.1')
        text_sample.tag_config("test", foreground='red')

    def input_field(self, window):
        text_input = tk.Text(window, width=50)
        text_input.config(font=("Arial", 14))
        text_input.grid(column=5, row=0, columnspan=5, padx=(0, 50), pady=50)
        text_input.focus()

    def display(self, text_to_show):
        window = tk.Tk()
        window.resizable(False, False)

        self.text_example(window, text_to_show)

        self.input_field(window)

        window.mainloop()


class SpeedTypingTest:
    def __init__(self, text_to_contest="test", test_duration=60):
        file = open("texts/" + text_to_contest + ".txt", 'r')
        self.text = file.read()
        self.duration = test_duration
        self.mistakes_idexes = []

    def interface(self):
        root = tk.Tk()
        root.geometry('400x250')

        def func(*args):
            t['text'] = e.get('1.0', 'end-1c')

        def func1(*args):
            print(time.monotonic())
            root.after(60000, func1)

        e = st.ScrolledText(root, height=3)
        func1()
        e.pack()
        e.focus()
        t = tk.Label(root)
        e.bind('<KeyRelease>', func)
        t.pack()
        root.mainloop()

    def speedTyping(self, typed_text):
        if self.text == typed_text:
            return 1


if __name__ == '__main__':
    sp = SpeedTypingInterface()
    sp.display(open("texts/" + "test" + ".txt", 'r').read())
    #print([open("texts/" + 'test' + ".txt", 'r').read()])
