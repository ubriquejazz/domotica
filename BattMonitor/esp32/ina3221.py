from machine import I2C, Pin

class INA3221:
    def __init__(self, scl_pin: int = 22, sda_pin: int = 21, i2c_id: int = 0, addr: int = 0x40, shunt_resistor: float = 0.1):
        # Configure pins and initialize the I2C peripheral
        self.scl = Pin(scl_pin)
        self.sda = Pin(sda_pin)
        self.i2c = I2C(i2c_id, scl=self.scl, sda=self.sda)
        self.addr = addr
        self.shunt = shunt_resistor

    def _read_reg(self, reg: int) -> int:
        raw = self.i2c.readfrom_mem(self.addr, reg, 2)
        return (raw[0] << 8) | raw[1]

    def get_bus_voltage(self, channel: int) -> float:
        if not 1 <= channel <= 3:
            raise ValueError("Channel must be 1, 2, or 3")
        reg = 0x02 + ((channel - 1) * 2)
        raw = self._read_reg(reg)
        if raw & 0x8000:
            raw -= 65536
        return (raw >> 3) * 0.001

    def get_shunt_voltage(self, channel: int) -> float:
        if not 1 <= channel <= 3:
            raise ValueError("Channel must be 1, 2, or 3")
        reg = 0x01 + ((channel - 1) * 2)
        raw = self._read_reg(reg)
        if raw & 0x8000:
            raw -= 65536
        return raw * 0.00004

    def get_current(self, channel: int) -> float:
        return self.get_shunt_voltage(channel) / self.shunt
