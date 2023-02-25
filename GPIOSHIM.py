import board
import digitalio
import pulseio
import busio


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
        
    def setmode(self, mode):
        self.mode = mode

    def getmode(self):
        return self.mode

    def setwarnings(self, flag):
        pass

    def setup(self, pin, mode, pull_up_down=None):
        if mode == GPIOSHIM.OUT:
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

    def set_i2c_bus(self, bus_number):
        i2c = busio.I2C(self.pin_mappings[SDA], self.pin_mappings[SCL], frequency=100000)
        self.pin_config[bus_number] = i2c

    def write_i2c_block_data(self, bus_number, address, data):
        if bus_number in self.pin_config:
            device = self.pin_config[bus_number].get_device(address)
            device.write(data)

    def set_spi_bus(self, bus_number, sck_pin, mosi_pin, miso_pin):
        spi = busio.SPI(self.pin_mappings[sck_pin], MOSI=self.pin_mappings[mosi_pin], MISO=self.pin_mappings[miso_pin])
        self.pin_config[bus_number] = spi

    def transfer_spi_data(self, bus_number, data):
        if bus_number in self.pin_config:
            with digitalio.DigitalInOut(self.pin_mappings[CS]) as cs:
                cs.switch_to_output(value=True)
                cs.value = False
                response = bytearray(len(data))
                self.pin_config[bus_number].write_readinto(data, response)
                cs.value = True
                return response

    def set_pwm_frequency(self, pin, frequency):
        if pin in self.pin_config:
            pwm = pulseio.PWMOut(self.pin_mappings[pin], frequency=frequency)
            self.pin_config[pin] = pwm

    def set_pwm_duty_cycle(self, pin, duty_cycle):
        if pin in self.pin_config:
            self.pin_config[pin].duty_cycle = duty_cycle


GPIO = GPIOSHIM()
