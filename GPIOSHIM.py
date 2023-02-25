import board
import digitalio
import logging


class GPIOSHIM:
    OUT = 0
    IN = 1
    LOW = 0
    HIGH = 1
    BCM = 0
    BOARD = 1
    PUD_OFF = "OFF"
    PUD_DOWN = "DOWN"
    PUD_UP = "UP"

    pin_mappings = {
        4: board.D4,
        5: board.D5,
        6: board.D6,
        7: board.D7,
        8: board.C0,
        9: board.C1,
        10: board.C2,
        11: board.C3,
        12: board.C4,
        13: board.C5,
        14: board.C6,
        15: board.C7
    }

    def __init__(self):
        self.pin_config = {}
        self.mode = None
        self._logger = logging.getLogger(__name__)

    def setmode(self, mode):
        self.mode = mode

    def getmode(self):
        return self.mode

    def setwarnings(self, flag):
        pass

    def setup(self, pin, mode, pull_up_down=None):
        self._logger.info(f"Setting up pin {pin} with mode {mode} and pull_up_down {pull_up_down}")
        if mode == GPIOSHIM.OUT:
            self._logger.info("setup OUTPUT pin")
            self.pin_config[pin] = digitalio.DigitalInOut(self.pin_mappings[pin])
            self.pin_config[pin].direction = digitalio.Direction.OUTPUT
        elif mode == GPIOSHIM.IN:
            self.pin_config[pin] = digitalio.DigitalInOut(self.pin_mappings[pin])
            self.pin_config[pin].direction = digitalio.Direction.INPUT
            if pull_up_down == GPIOSHIM.PUD_UP:
                self.pin_config[pin].pull = digitalio.Pull.UP
            elif pull_up_down == GPIOSHIM.PUD_DOWN:
                self.pin_config[pin].pull = digitalio.Pull.DOWN

    def output(self, pin, state):
        self._logger.info("setup output GPIO")
        if pin in self.pin_config:
            self.pin_config[pin].value = state

    def input(self, pin):
        if pin in self.pin_config:
            return self.pin_config[pin].value

    def cleanup(self, pin=None):
        if pin is None:
            for p in self.pin_config:
                del self.pin_config[p]
        elif pin in self.pin_config:
            self.pin_config[pin].deinit()
            del self.pin_config[pin]


GPIO = GPIOSHIM()
