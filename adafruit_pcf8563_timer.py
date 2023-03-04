# SPDX-FileCopyrightText: 2016 Philip R. Moyer and Radomir Dopieralski for Adafruit Industries.
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Bernhard Bablok
#
# SPDX-License-Identifier: MIT

"""
`adafruit_pcf8563_timer` - PCF8563 Timer module
===============================================

This class supports the timer of the PCF8563-based RTC in CircuitPython.

Functions are included for reading and writing registers and manipulating
timer objects.

The class supports stand-alone usage. In this case, pass an i2-bus object
to the constructor. If used together with the PCF8563 class (rtc), instantiate
the rtc-object first and then pass the i2c_device attribute of the rtc
to the constructor of the timer.

Author(s): Bernhard Bablok
Date: November 2023

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


class PCF8563_Timer:  # pylint: disable=too-few-public-methods
    """Interface to the timer of the PCF8563 RTC.

    :param I2C i2c_bus: The I2C bus object
    """

    timer_enabled = i2c_bit.RWBit(0x0E, 7)
    """True if the timer is enabled. Default is False."""

    timer_frequency = i2c_bits.RWBits(2, 0x0E, 0)
    """Timer clock frequency. Default is 1/60Hz.
    Possible values are as shown (selection value - frequency).
    00 - 4.096kHz
    01 - 64Hz
    10 -  1Hz
    11 -  1/60Hz
    """
    TIMER_FREQ_4KHZ = const(0b00)
    """Timer frequency of 4 KHz"""
    TIMER_FREQ_64HZ = const(0b01)
    """Timer frequency of 64 Hz"""
    TIMER_FREQ_1HZ = const(0b10)
    """Timer frequency of 1 Hz"""
    TIMER_FREQ_1_60HZ = const(0b11)
    """Timer frequency of 1/60 Hz"""

    timer_value = i2c_bits.RWBits(8, 0x0F, 0)
    """ Timer value (0-255). The default is undefined.
    The total countdown duration is calcuated by
    timer_value/timer_frequency. For a higher precision, use higher values
    and frequencies, e.g. for a one minute timer you could use
    value=1, frequency=1/60Hz or value=60, frequency=1Hz. The
    latter will give better results. See the PCF85x3 User's Manual
    for details."""

    timer_interrupt = i2c_bit.RWBit(0x01, 0)
    """True if the interrupt pin will assert when timer has elapsed.
    Defaults to False."""

    timer_status = i2c_bit.RWBit(0x01, 2)
    """True if timer has elapsed. Set to False to reset."""

    timer_pulsed = i2c_bit.RWBit(0x01, 4)
    """True if timer asserts INT as a pulse. The default
    value False asserts INT permanently."""

    def __init__(self, i2c: Union[I2C, I2CDevice]) -> None:
        time.sleep(0.05)
        if isinstance(i2c, I2CDevice):
            self.i2c_device = i2c  # reuse i2c_device (from PCF8563-instance)
        else:
            self.i2c_device = I2CDevice(i2c, 0x51)
