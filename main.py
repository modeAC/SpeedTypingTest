from model import SpeedTypingInternals
from view import SpeedTypingInterfaceGUI, SpeedTypingInterfaceCmd
from presenter import SpeedTypingManager
from utils import AvailableTexts

if __name__ == '__main__':
    duration = 60
    text = AvailableTexts.text1
    is_shell = True

    internals = SpeedTypingInternals(test_duration=duration, text_to_contest=text.value)
    if is_shell:
        interface = SpeedTypingInterfaceCmd(text=internals.text, duration=duration)
    else:
        interface = SpeedTypingInterfaceGUI(text=internals.text, duration=duration)

    s = SpeedTypingManager(internals, interface, duration)
