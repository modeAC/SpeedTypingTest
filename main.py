# This is a sample Python script.
import tkinter
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import tkinter as tk
import time
import enum
import random


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


class pseudoPointer:
    def __init__(self, var=None):
        self.value = [var]

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


# def compare_strings(str1, str2, start, stop):
#     mistakes = []
#     if str1 == str2:
#         return 1
#     for i in range(start, stop):
#         if str1[i] != str2[i]:
#             mistakes.append(i)
#     return ((mistakes, 1)[len(mistakes) == 0])

def compare_strings(str1, str2, start, stop):
    mistakes = 0
    if str1 == str2:
        return 0
    for i in range(start, stop):
        if str1[i] != str2[i]:
            mistakes+=1
    return mistakes


class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = 0

    def start(self):
        self.start_time = time.monotonic()

    def update(self):
        if time.monotonic() - self.start_time >= self.duration:
            return self.duration
        return (time.monotonic() - self.start_time)


class SpeedTypingInternals:
    def __init__(self, text_to_contest=_choose_text(), test_duration=60):
        file = open("texts/" + text_to_contest + ".txt", 'r')
        self.text = stringPlus(file.read())
        self.duration = test_duration
        self.mistakes_indexes = []

    def speed_typing_check(self, typed_text, start, stop):
        if self.text == typed_text:
            return 1
        try:
            self.mistakes_indexes = compare_strings(self.text.string, typed_text, start, stop)
            return 0
        except IndexError:
            raise IndexError("start or stop index out of range")


class SpeedTypingInterface():
    def __init__(self):
        self.duration = 15.0
        self.time = Timer(self.duration)
        self.start_flag = False
        self.timer_started = False
        self.finish_flag = False
        self.popup_crated = False

    @staticmethod
    def highlight_text(txtwidget, tag_name, lineno, start_char, end_char, bg_color=None, fg_color=None):
        txtwidget.tag_add(tag_name, f'{lineno}.{start_char}', f'{lineno}.{end_char}')
        txtwidget.tag_config(tag_name, background=bg_color, foreground=fg_color)

    def __reset(self):
        self.start_flag = False
        self.timer_started = False
        self.finish_flag = False
        self.popup_crated = False

    def timer(self, window):
        if self.start_flag is True:
            self.time.start()
        label = tk.Label(window, text='0.00', font=("Arial", 14))
        label.grid(row=1, column=0, pady=(0, 50))

        def func():
            if self.start_flag is True:
                label['text'] = "{0:.2f}".format(self.time.update())
                if self.time.update() == self.duration:
                    self.start_flag = False
                    self.finish_flag = True
                    return
                window.after(50, func)
        func()


    def text_example(self, window, text_to_show):
        text_sample = tk.Text(window, width=50)
        text_sample.insert('0.0', text_to_show)
        text_sample.grid(column=0, row=0, columnspan=5, padx=50, pady=50)
        text_sample.config(state=tk.DISABLED, font=("Arial", 14))
        text_sample.tag_add("test", '1.0', '1.1')
        text_sample.tag_config("test", foreground='red')

    def __game_started(self, text_input):
        if text_input.get('1.0', 'end-1c') == "":
            return False
        return True

    def input_field(self, window, text_var):
        text_input = tk.Text(window, width=50)
        text_input.config(font=("Arial", 14))
        text_input.grid(column=5, row=0, columnspan=5, padx=(0, 50), pady=50)
        text_input.focus()

        def func():
            text_var.set_value(text_input.get('1.0', 'end-1c'))
            if self.__game_started(text_input) is True:
                self.start_flag = True
            if self.finish_flag is True:
                text_input.delete("1.0","end")
            window.after(10, func)

        func()

    def popup_window(self, text_var):
        message = "Keyspeed is " + str(len(text_var.get_value())) + "KPM\nNumber of mistakes is " + str(compare_strings(open("texts/" + "test" + ".txt", 'r').read(), text_var.get_value(), 0, len(text_var.get_value())))
        popup = tk.Toplevel()
        popup.resizable(False, False)
        label = tk.Label(popup, text=message).pack(padx=50, pady=50)

        def func():
            self.start_flag = False
            self.timer_started = False
            self.finish_flag = False
            self.popup_crated = False
            self.time = Timer(5)
            popup.destroy()

        tk.Button(popup, text="reset", command=func).pack()

        popup.mainloop()


    def display(self, text_to_show, text_var):

        window = tk.Tk()
        window.resizable(False, False)

        self.text_example(window, text_to_show)

        self.input_field(window, text_var)

        self.timer(window)

        while True:
            try:
                window.update()
                print(self.start_flag)
                if self.start_flag is True and self.finish_flag is False:
                    #print(text_var.get_value())
                    if self.timer_started is False:
                        self.timer(window)
                        self.timer_started = True
                if self.finish_flag is True:
                    if self.popup_crated is False:
                        self.popup_window(text_var)
                        self.popup_crated = True

            except tk.TclError:
                break

        #window.mainloop()




if __name__ == '__main__':
    text_var = pseudoPointer("")
    sp = SpeedTypingInterface()
    sp.display(open("texts/" + "test" + ".txt", 'r').read(), text_var)
    # s = stringPlus("you\nare\nfucked")
    # print(s.info)
    # print(s.string)
