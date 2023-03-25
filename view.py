import time
import tkinter as tk
import threading as th

from pynput import keyboard

from utils import stringPlus


class SpeedTypingInterface(th.Thread):
    started: bool = None
    typed_text: str = None

    def __init__(self, text=stringPlus(""), duration=60):
        super(SpeedTypingInterface, self).__init__()
        pass

    def run(self):
        pass

    def set_time(self, time):
        pass

    def set_mistake_indexes(self, indexes):
        pass

    def set_typos_number(self, number):
        pass


class SpeedTypingInterfaceGUI(SpeedTypingInterface):
    def __init__(self, text=stringPlus(""), duration=60):
        super(SpeedTypingInterfaceGUI, self).__init__(text, duration)
        self.duration = duration
        self.timer_value = 0
        self.started = False

        self.text_to_show = text
        self.typed_text = ''
        self.sample_end_index = text.reformat_index(len(self.text_to_show))
        self.input_end_index = None
        self.typos = 0
        self.mistakes_indexes = set()

        self.finish_game = False

        self.window = None
        self.text_sample = None
        self.text_input = None
        self.timer = None

    def run(self):
        self.__interface()

    def set_time(self, time):
        self.timer_value = time

    def set_mistake_indexes(self, indexes):
        self.mistakes_indexes = indexes

    def set_typos_number(self, number):
        self.typos = number

    @staticmethod
    def __highlight_text(txtwidget, tag_name, start_line, end_line, start_char, end_char, bg_color=None, fg_color=None):
        txtwidget.tag_add(tag_name, f'{start_line}.{start_char}', f'{end_line}.{end_char}')
        txtwidget.tag_config(tag_name, background=bg_color, foreground=fg_color)

    @staticmethod
    def __highlight_overtype(txtwidget, tag_name, start_line, start_char, bg_color=None):
        txtwidget.tag_add(tag_name, f'{start_line}.{start_char}', 'end')
        txtwidget.tag_config(tag_name, background=bg_color)

    def __highlight_mistakes(self, mistakes):
        if not mistakes:
            return
        else:
            for index in mistakes:
                self.__highlight_text(self.text_sample, 'mistake', index[0], index[0], index[1], index[1] + 1,
                                      bg_color='#FDCDC2', fg_color='red')

    def __highlight(self):
        mistakes_indexes = {self.text_to_show.reformat_index(ind) for ind in self.mistakes_indexes}
        self.input_end_index = self.text_to_show.reformat_index(len(self.typed_text) - self.typed_text.count('\n'))
        for tag in self.text_sample.tag_names():
            self.text_sample.tag_delete(tag)
        for tag in self.text_input.tag_names():
            self.text_input.tag_delete(tag)
        try:
            self.__highlight_text(self.text_sample, "correct_input", 1, self.input_end_index[0], 0,
                                  self.input_end_index[1], fg_color='green')
            self.__highlight_mistakes(mistakes_indexes)
        except TypeError:
            self.__highlight_text(self.text_sample, "correct_input", 0, self.sample_end_index[0], 0,
                                  self.sample_end_index[1],
                                  fg_color='green')
            self.__highlight_overtype(self.text_input, 'overtype', self.sample_end_index[0],
                                      self.sample_end_index[1], bg_color='#FDCDC2')
            self.__highlight_mistakes(mistakes_indexes)

    def __text_sample_config(self):
        self.text_sample.insert('0.0', self.text_to_show)
        self.text_sample.grid(column=0, row=0, columnspan=5, padx=50, pady=50)
        self.text_sample.config(state=tk.DISABLED, font=("Arial", 14))

    def __text_input_config(self):
        self.text_input.config(font=("Arial", 14))
        self.text_input.grid(column=5, row=0, columnspan=5, padx=(0, 50), pady=50)
        self.text_input.focus()

    def __popup_window(self, speed, mistakes_number):
        message = "Keyspeed is " + str(speed) + " KPM\nNumber of mistakes is " + str(
            mistakes_number) + "\nNumber of corrections is " + str(self.typos)
        popup = tk.Toplevel()
        popup.resizable(False, False)
        label = tk.Label(popup, text=message).pack(padx=50, pady=50)

        def closeAll():
            self.window.destroy()

        tk.Button(popup, text="Close", command=closeAll).pack()
        popup.mainloop()

    def __timer_update(self, current_time):
        self.timer['text'] = "{0:.0f}".format(current_time)

    def __is_game_started(self):
        if self.text_input.get('1.0', 'end-1c') == "":
            return False
        return True

    def __interface(self):
        self.window = tk.Tk()
        self.window.resizable(False, False)

        self.text_sample = tk.Text(self.window, width=50)
        self.__text_sample_config()

        self.text_input = tk.Text(self.window, width=50)
        self.__text_input_config()

        self.timer = tk.Label(self.window, text='0.00', font=("Arial", 14))
        self.timer.grid(row=1, column=0, pady=(0, 50))

        while True:
            try:
                if not self.started:
                    self.started = self.__is_game_started()
                if self.finish_game:
                    self.__popup_window(int(len(self.typed_text) * self.duration / self.timer_value),
                                        len(self.mistakes_indexes))
                self.typed_text = self.text_input.get('1.0', 'end-1c')
                self.__highlight()
                self.__timer_update(self.timer_value)
                self.window.update()
            except tk.TclError:
                return


class SpeedTypingInterfaceCmd(SpeedTypingInterface):
    def __init__(self, text=stringPlus(""), duration=60):
        super(SpeedTypingInterfaceCmd, self).__init__()
        self.text_to_show = text
        self.typed_text = ''

        self.typos = 0
        self.mistakes_indexes = set()

        self.duration = duration
        self.timer_value = 0

        self.started = False
        self.finish_game = False

    def run(self):
        self.__interface()

    def set_time(self, time):
        self.timer_value = time

    def set_mistake_indexes(self, indexes):
        self.mistakes_indexes = indexes

    def set_typos_number(self, number):
        self.typos = number

    def __on_release(self, key):
        if key == keyboard.Key.backspace:
            self.typed_text = self.typed_text[:-1]
        elif key == keyboard.Key.space:
            self.typed_text += ' '
        else:
            try:
                self.typed_text += f'{key.char}'
            except Exception:
                pass
        if self.finish_game:
            return False

    @staticmethod
    def __countdown():
        print('3')
        time.sleep(1)
        print('2')
        time.sleep(1)
        print('1')
        time.sleep(1)
        print('start typing')

    def __interface(self):
        print(self.text_to_show)
        print('\nwait till countdown')

        listener = keyboard.Listener(on_release=self.__on_release)
        self.__countdown()
        if not self.started:
            self.started = True
        listener.start()

        while not self.finish_game:
            pass

        print(f'\nkeyspeed is {int(len(self.typed_text) * self.duration / self.timer_value)} KPM\ntypos nr: {self.typos}')


