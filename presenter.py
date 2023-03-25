from model import SpeedTypingInternals
from utils import Timer
from view import SpeedTypingInterface


class SpeedTypingManager:
    def __init__(self, internals: SpeedTypingInternals, interface: SpeedTypingInterface, duration: int = 60):
        self.timer = Timer(duration)
        self.internals = internals
        self.interface = interface
        self.interface.start()

        while self.interface.is_alive():
            if self.interface.started:
                if not self.timer.started:
                    self.timer.start()
                self.interface.set_time(self.timer.update())
                self.internals.set_time(self.timer.update())
                if self.internals.speed_typing_check(self.interface.typed_text):
                    self.interface.set_typos_number(self.internals.get_typos())
                    self.interface.finish_game = True

                self.interface.set_mistake_indexes(self.internals.get_mistakes_indexes())
