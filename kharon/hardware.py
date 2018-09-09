# LED, Analog_Pin, Digital_pin, Switch, Pushbutton

OUT = 'OUTPUT'
IN = 'INPUT'
HIGH = 'HIGH'
LOW = 'LOW'


class Hardware:
    c = ''
    requires = ''
    name = ''

    def __init__(self):
        pass

    def declaration(self):
        return ''

    def setup(self):
        return ''


class AnalogPin(Hardware):
    c = ''

    def __init__(self, pin_number, mode):
        self.pin_number = pin_number
        self.mode = mode
        super(AnalogPin, self).__init__()

    def setup(self):
        return 'pinMode(%d, %s);' % (self.pin_number, self.mode)

    def read(self):
        return 'analogRead(%d' % self.pin_number


class DigitalPin(Hardware):
    c = ''

    def __init__(self, pin_number, mode):
        self.pin_number = pin_number
        self.mode = mode
        super(DigitalPin, self).__init__()

    def setup(self):
        return 'pinMode(%d, %s);' % (self.pin_number, self.mode)

    def write(self, mode=LOW):
        return 'digitalWrite(%d, ' % self.pin_number

    def read(self):
        return 'digitalRead(%d' % self.pin_number


class Servo(Hardware):
    c = ''
    requires = '#include <Servo.h>'

    def __init__(self, pin_number):
        self.pin_number = pin_number
        super(Servo, self).__init__()

    def declaration(self):
        return 'Servo %s;' % self.name

    def setup(self):
        return '%s.attach(%d);' % (self.name, self.pin_number)

    def write(self, angle=0):
        return '%s.write(' % self.name


HARDWARE = [AnalogPin, DigitalPin, Servo]
