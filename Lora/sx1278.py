from machine import Pin
import time

class SX1278:
    def __init__(self, spi, cs, rst, freq=433E6, power=17):
        self.spi = spi
        self.cs = Pin(cs, Pin.OUT, value=1)
        self.rst = Pin(rst, Pin.OUT, value=1)

        self.rst.value(0); time.sleep_ms(10)
        self.rst.value(1); time.sleep_ms(10)

        if self._r(0x42) != 0x12:
            raise RuntimeError("SX1278 not found - check wiring")

        self._w(0x01, 0x80)                      # sleep + LoRa mode
        frf = int((freq * (1 << 19)) / 32000000)
        self._w(0x06, (frf >> 16) & 0xFF)
        self._w(0x07, (frf >> 8) & 0xFF)
        self._w(0x08, frf & 0xFF)
        self._w(0x09, 0x80 | (power - 2))        # PA_BOOST
        self._w(0x0C, self._r(0x0C) | 0x03)      # LNA boost
        self._w(0x1D, 0x72)                      # BW125, CR4/5, explicit header
        self._w(0x1E, 0x74)                      # SF7, CRC on
        self._w(0x26, 0x04)                      # AGC auto
        self._w(0x39, 0x12)                      # sync word
        self._w(0x0E, 0x00)                      # TX FIFO base
        self._w(0x0F, 0x00)                      # RX FIFO base
        self._w(0x01, 0x81)                      # standby

    def _r(self, reg):
        self.cs.value(0)
        self.spi.write(bytearray([reg & 0x7F]))
        v = self.spi.read(1)[0]
        self.cs.value(1)
        return v

    def _w(self, reg, val):
        self.cs.value(0)
        self.spi.write(bytearray([reg | 0x80, val]))
        self.cs.value(1)

    def send(self, msg):
        if isinstance(msg, str):
            msg = msg.encode()
        self._w(0x01, 0x81)
        self._w(0x0D, 0x00)
        for b in msg:
            self._w(0x00, b)
        self._w(0x22, len(msg))
        self._w(0x12, 0xFF)
        self._w(0x01, 0x83)                      # TX
        t = time.ticks_ms()
        while not (self._r(0x12) & 0x08):        # TxDone
            if time.ticks_diff(time.ticks_ms(), t) > 3000:
                break
        self._w(0x12, 0xFF)
        self._w(0x01, 0x81)

    def listen(self):
        self._w(0x01, 0x85)                      # continuous RX

    def receive(self):
        """Returns a string if a packet arrived, else None."""
        irq = self._r(0x12)
        if not (irq & 0x40):                     # RxDone
            return None
        self._w(0x12, 0xFF)
        if irq & 0x20:                           # CRC error
            return None
        n = self._r(0x13)
        self._w(0x0D, self._r(0x10))
        data = bytearray(self._r(0x00) for _ in range(n))
        try:
            return data.decode()
        except:
            return None
