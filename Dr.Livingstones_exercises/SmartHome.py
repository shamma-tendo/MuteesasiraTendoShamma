class SmartDevice:
    def __init__(self, device_id):
        self.device_id = device_id
        self.is_on     = False

    def turn_on(self):
        self.is_on = True
        print(f"{self.device_id} ON")

    def turn_off(self):
        self.is_on = False
        print(f"{self.device_id} OFF")


class SmartLight(SmartDevice):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.brightness = 50

    def set_brightness(self, level):
        self.brightness = level
        print(f"Brightness set to {level}%")


class SmartThermostat(SmartDevice):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.temperature = 22

    def set_temperature(self, temp):
        self.temperature = temp
        print(f"Temperature set to {temp}°C")

light = SmartLight("LIGHT-01")
light.turn_on()
light.set_brightness(80)

thermo = SmartThermostat("THERMO-01")
thermo.turn_on()
thermo.set_temperature(20)