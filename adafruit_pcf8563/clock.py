# SPDX-FileCopyrightText: 2016 Philip R. Moyer and Radomir Dopieralski for Adafruit Industries.
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Bernhard Bablok
#
# SPDX-License-Identifier: MIT

"""
`clock` - PCF8563 Clock module
==============================

This class supports the clkout-feature of the PCF8563-based RTC in CircuitPython.

Functions are included for reading and writing registers to configure
clklout frequency.

The class supports stand-alone usage. In this case, pass an i2-bus object
to the constructor. If used together with the PCF8563 class (rtc), instantiate
the rtc-object first and then pass the i2c_device attribute of the rtc
to the constructor of the clock.

Author(s): Bernhard Bablok
Date: March 2023

Implementation Notes
--------------------

**Hardware:**

* `Seeeduino XIAO Expansion Board <https://www.adafruit.com/product/5033>`_
  - Works With Adafruit QT Py (Product ID: 5033)

**Software and Dependencies:**

* Adafruit CircuitPython firmware: https://github.com/adafruit/circuitpython/releases
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

**Notes:**

#. Datasheet: http://cache.nxp.com/documents/data_sheet/PCF8563.pdf
"""

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_PCF8563.git"

import time

from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register import i2c_bit
from adafruit_register import i2c_bits
from micropython import const

try:
    from typing import Union
    from busio import I2C
except ImportError:
    pass


class Clock:  # pylint: disable=too-few-public-methods
    """Interface to the clkout of the PCF8563 RTC.

    :param I2C i2c_bus: The I2C bus object
    """

    clockout_enabled = i2c_bit.RWBit(0x0D, 7)
    """True if clockout is enabled (default). To disable clockout, set to False"""

    clockout_frequency = i2c_bits.RWBits(2, 0x0D, 0)
    """Clock output frequencies generated. Default is 32.768kHz.
    Possible values are as shown (selection value - frequency).
    00 - 32.768khz
    01 - 1.024kHz
    10 - 0.032kHz (32Hz)
    11 - 0.001kHz (1Hz)
    """

    CLOCKOUT_FREQ_32KHZ = const(0b00)
    """Clock frequency of 32 KHz"""
    CLOCKOUT_FREQ_1KHZ = const(0b01)
    """Clock frequency of  4 KHz"""
    CLOCKOUT_FREQ_32HZ = const(0b10)
    """Clock frequency of 32 Hz"""
    CLOCKOUT_FREQ_1HZ = const(0b11)
    """Clock frequency of 1 Hz"""

    def __init__(self, i2c: Union[I2C, I2CDevice]) -> None:
        if isinstance(i2c, I2CDevice):
            self.i2c_device = i2c  # reuse i2c_device (from PCF8563-instance)
        else:
            time.sleep(0.05)
            self.i2c_device = I2CDevice(i2c, 0x51)
