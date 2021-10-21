# This is a sample Python script.
import tkinter
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import tkinter as tk
import time
import enum
import random
import threading as th


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

    def __getitem__(self, item):
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
        lenght = len(str1)
    else:
        lenght = len(str2)

    for i in range(lenght):
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
        return (time.monotonic() - self.start_time)


class SpeedTypingInternals:
    def __init__(self, text_to_contest=_choose_text(), test_duration=60):
        file = open("texts/" + text_to_contest + ".txt", 'r')
        self.text = stringPlus(file.read())
        self.typed_text = stringPlus('')
        self.duration = test_duration
        self.timer_value = 0
        self.mistakes_indexes = set()
        self.typos = 0

    def count_typos(self, new_mistakes):
        diff = new_mistakes - self.mistakes_indexes
        self.typos += len(diff)

    def speed_typing_check(self, typed_text):
        if self.text.string == typed_text:
            return 1
        new_mistakes = compare_strings(self.text.string, typed_text)
        self.count_typos(new_mistakes)
        self.mistakes_indexes = [self.text.reformat_index(ind) for ind in new_mistakes]
        return 0

    def set_typed_text(self, text):
        self.typed_text = text

    def set_timer_value(self, time):
        self.timer_value = time

    def game_controller(self):
        while self.timer_value <= self.duration:
            if self.speed_typing_check(self.typed_text) == 1:
                break
        return 1


class SpeedTypingInterface(th.Thread):
    def __init__(self, text=stringPlus("")):
        th.Thread.__init__(self)
        self.text_to_show = text
        self.end_index = text.reformat_index(len(self.text_to_show))
        self.typed_text = ''
        self.timer_value = 0
        self.started = 0

        self.window = None
        self.text_sample = None
        self.text_input = None
        self.timer = None

    @staticmethod
    def highlight_text(txtwidget, tag_name, start_line, end_line, start_char, end_char, bg_color=None, fg_color=None):
        txtwidget.tag_add(tag_name, f'{start_line}.{start_char}', f'{end_line}.{end_char}')
        txtwidget.tag_config(tag_name, background=bg_color, foreground=fg_color)

    @staticmethod
    def highlight_overtype(txtwidget, tag_name, start_line, start_char, bg_color=None):
        txtwidget.tag_add(tag_name, f'{start_line}.{start_char}', 'end')
        txtwidget.tag_config(tag_name, background=bg_color)

    def highlight_mistakes(self, mistakes):
        if not mistakes:
            return
        else:
            for index in mistakes:
                self.highlight_text(self.text_sample, 'mistake', index[0], index[0], index[1], index[1] + 1,
                                    bg_color='#FDCDC2', fg_color='red')

    def highlight(self, end_index, mistakes):
        try:
            self.highlight_text(self.text_sample, "correct_input", 0, end_index[0], 0, end_index[1], fg_color='green')
            self.highlight_mistakes(mistakes)
        except TypeError:
            self.highlight_text(self.text_sample, "correct_input", 0, self.end_index[0], 0, self.end_index[1],
                                fg_color='green')
            self.highlight_overtype(self.text_input, 'overtype', self.end_index[0], self.end_index[1],
                                    bg_color='#FDCDC2')
            self.highlight_mistakes(mistakes)

    def text_sample_config(self):
        self.text_sample.insert('0.0', self.text_to_show)
        self.text_sample.grid(column=0, row=0, columnspan=5, padx=50, pady=50)
        self.text_sample.config(state=tk.DISABLED, font=("Arial", 14))

    def text_input_config(self):
        self.text_input.config(font=("Arial", 14))
        self.text_input.grid(column=5, row=0, columnspan=5, padx=(0, 50), pady=50)
        self.text_input.focus()

    def timer_update(self, current_time):
        self.timer['text'] = "{0:.0f}".format(current_time)

    def __game_started(self):
        if self.text_input.get('1.0', 'end-1c') == "":
            return False
        return True

    def set_time(self, time):
        self.timer_value = time

    def interface(self):
        #timer = Timer(10)
        self.window = tk.Tk()
        self.window.resizable(False, False)

        self.text_sample = tk.Text(self.window, width=50)
        self.text_sample_config()

        self.text_input = tk.Text(self.window, width=50)
        self.text_input_config()

        self.timer = tk.Label(self.window, text='0.00', font=("Arial", 14))
        self.timer.grid(row=1, column=0, pady=(0, 50))

        while True:
            try:
                self.started = self.__game_started()
                self.typed_text = stringPlus(self.text_input.get('1.0', 'end-1c'))
                self.timer_update(self.timer_value)
                self.window.update()
            except tk.TclError:
                return

    def run(self):
        self.interface()


class SpeedTypingManager:
    def __init__(self, duration=10):
        self.timer = Timer(duration)
        self.internals = SpeedTypingInternals(test_duration=duration)
        self.interface = SpeedTypingInterface(text=self.internals.text)
        self.interface.start()

        while self.interface.is_alive():
            if self.interface.started:
                if not self.timer.started:
                    self.timer.start()
                self.interface.set_time(self.timer.update())



class SpeedTypingInterface_old:
    def __init__(self, test_duration=60, text=stringPlus("")):
        self.text_to_show = text
        self.duration = test_duration
        self.time = Timer(self.duration)
        self.start_flag = False
        self.timer_started = False
        self.finish_flag = False
        self.popup_crated = False
        self.end_index = self.text_to_show.reformat_index(len(self.text_to_show.string))

    @staticmethod
    def highlight_text(txtwidget, tag_name, start_line, end_line, start_char, end_char, bg_color=None, fg_color=None):
        txtwidget.tag_add(tag_name, f'{start_line}.{start_char}', f'{end_line}.{end_char}')
        txtwidget.tag_config(tag_name, background=bg_color, foreground=fg_color)

    @staticmethod
    def highlight_background(txtwidget, tag_name, start_line, start_char, bg_color=None):
        txtwidget.tag_add(tag_name, f'{start_line}.{start_char}', 'end')
        txtwidget.tag_config(tag_name, background=bg_color)

    def highlight_entered_text(self, text_field, end_index, text_var):
        try:
            self.highlight_text(text_field, "correct_input", 0, end_index[0], 0, end_index[1], fg_color='green')
            self.highlight_mistakes(text_field, text_var)
        except TypeError:
            self.highlight_text(text_field, "correct_input", 0, self.end_index[0], 0, self.end_index[1],
                                fg_color='green')
            self.highlight_mistakes(text_field, text_var)

    def highlight_mistakes(self, text_field, text_var):
        mistakes = compare_strings(self.text_to_show.string, text_var.get_value())
        if not mistakes:
            return
        else:
            for mist in mistakes:
                index = self.text_to_show.reformat_index(mist)
                self.highlight_text(text_field, 'mistake', index[0], index[0], index[1], index[1] + 1,
                                    bg_color='#FDCDC2', fg_color='red')

    def __finish(self):
        self.start_flag = False
        self.finish_flag = True

    def timer(self, window):
        if self.start_flag is True:
            self.time.start()
        label = tk.Label(window, text='0.00', font=("Arial", 14))
        label.grid(row=1, column=0, pady=(0, 50))

        def func():
            if self.start_flag is True:
                label['text'] = "{0:.2f}".format(self.time.update())
                if self.time.update() == self.duration or self.finish_flag == True:
                    self.__finish()
                    return
                window.after(50, func)

        func()

    def text_example(self, window, text_to_show, text_var):
        text_sample = tk.Text(window, width=50)
        text_sample.insert('0.0', text_to_show)
        text_sample.grid(column=0, row=0, columnspan=5, padx=50, pady=50)
        text_sample.config(state=tk.DISABLED, font=("Arial", 14))

        def func():
            end_index = self.text_to_show.reformat_index(len(text_var))
            for tag in text_sample.tag_names():
                text_sample.tag_delete(tag)
            self.highlight_entered_text(text_sample, end_index, text_var)
            text_sample.update()
            if self.finish_flag is True:
                return
            window.after(50, func)

        func()

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
            for tag in text_input.tag_names():
                text_input.tag_delete(tag)
            text_var.set_value(text_input.get('1.0', 'end-1c'))
            if self.__game_started(text_input) is True:
                self.start_flag = True
            if self.finish_flag is True:
                text_input.delete("1.0", "end")
                return
            if len(self.text_to_show.string) < len(text_var):
                index = self.text_to_show.reformat_index(len(self.text_to_show.string))
                self.highlight_background(text_input, "overtype", index[0], index[1], bg_color='#FDCDC2')
            window.after(50, func)

        func()

    def popup_window(self, text_var, speed, mistakes_number, window):
        message = "Keyspeed is " + str(speed) + " KPM\nNumber of mistakes is " + str(mistakes_number)
        popup = tk.Toplevel()
        popup.resizable(False, False)
        label = tk.Label(popup, text=message).pack(padx=50, pady=50)

        def func():
            self.start_flag = False
            self.timer_started = False
            self.finish_flag = False
            self.popup_crated = False
            self.time = Timer(self.duration)
            window.destroy()

        tk.Button(popup, text="Close", command=func).pack()

        popup.mainloop()

    def start(self, window, text_var):
        window.resizable(False, False)

        self.text_example(window, self.text_to_show.string, text_var)

        self.input_field(window, text_var)

        self.timer(window)

    def display(self, text_var):

        window = tk.Tk()
        self.start(window, text_var)

        while True:
            if count_mistakes(self.text_to_show.string, text_var.get_value()) is True:
                time = self.time.update()
                self.__finish()
            try:
                window.update()
                if self.start_flag is True and self.finish_flag is False:
                    if self.timer_started is False:
                        self.timer(window)
                        self.timer_started = True
                if self.finish_flag is True:
                    if self.popup_crated is False:
                        mistakes_number = count_mistakes(self.text_to_show.string, text_var.get_value())
                        speed = len(text_var.get_value())
                        if mistakes_number is True:
                            mistakes_number = 0
                            try:
                                speed = int(len(text_var.get_value()) * 60 // time)
                            except ZeroDivisionError:
                                speed = "OVER 9000"
                        self.popup_window(text_var, speed, mistakes_number, window)
                        self.popup_crated = True


            except tk.TclError:
                break

        # window.mainloop()
class SpeedTypingManager_old:
    def __init__(self):
        self.internals = SpeedTypingInternals()
        self.interface = SpeedTypingInterface_old(text=SpeedTypingInternals().text,
                                               test_duration=self.internals.duration)

    def start(self):
        text_var = pseudoPointer("")
        self.interface.display(text_var)


if __name__ == '__main__':
    s = SpeedTypingManager()
    # s = SpeedTypingInterface(stringPlus('123'))
    # s.start()
    # timer = Timer(10)
    #
    # while True:
    #     if s.started:
    #         if not timer.started:
    #             timer.start()
    #         s.set_time(timer.update())
    #     print(s.typed_text)