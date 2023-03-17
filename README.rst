
Introduction to Adafruit's PCF8563 Real Time Clock (RTC) Library
================================================================

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-pcf8563/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/pcf8563/en/latest/
    :alt: Documentation Status

.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_PCF8563/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_PCF8563/actions/
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

This is a great battery-backed real time clock (RTC) that allows your
microcontroller project to keep track of time even if it is reprogrammed,
or if the power is lost. Perfect for datalogging, clock-building, time
stamping, timers and alarms, etc.

The PCF8563 is simple and inexpensive but not a high precision device.
It may lose or gain multiple seconds a day. For a high-precision,
temperature compensated alternative, please check out the
`DS3231 precision RTC. <https://www.adafruit.com/products/3013>`_
If you need a DS1307 for compatibility reasons, check out our
`DS1307 RTC breakout <https://www.adafruit.com/products/3296>`_.

Dependencies
=============

This driver depends on the `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_
and `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
libraries. Please ensure they are also available on the CircuitPython filesystem.
This is easily achieved by downloading
`a library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================
On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-pcf8563/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-pcf8563

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-pcf8563

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install adafruit-circuitpython-pcf8563


Usage Notes
===========

Basics
------

Of course, you must import the library to use it:

.. code:: python

    import busio
    from adafruit_pcf8563.pcf8563 import PCF8563
    import time

All the Adafruit RTC libraries take an instantiated and active I2C object
(from the `busio` library) as an argument to their constructor. The way to
create an I2C object depends on the board you are using. For boards with labeled
SCL and SDA pins, you can:

.. code:: python

    from board import *

Now, to initialize the I2C bus:

.. code:: python

    i2c_bus = board.I2C()

Once you have created the I2C interface object, you can use it to instantiate
the RTC object:

.. code:: python

    rtc = PCF8563(i2c_bus)

Date and time
-------------

To set the time, you need to set ``datetime`` to a `time.struct_time` object:

.. code:: python

    rtc.datetime = time.struct_time((2017,1,9,15,6,0,0,9,-1))

After the RTC is set, you retrieve the time by reading the `datetime`
attribute and access the standard attributes of a struct_time such as ``tm_year``,
``tm_hour`` and ``tm_min``.

.. code:: python

    t = rtc.datetime
    print(t)
    print(t.tm_hour, t.tm_min)

Alarm
-----

To set the time, you need to set `alarm` to a tuple with a `time.struct_time`
object and string representing the frequency such as "hourly":

.. code:: python

    rtc.alarm = (time.struct_time((2017,1,9,15,6,0,0,9,-1)), "daily")

After the RTC is set, you retrieve the alarm status by reading the
`alarm_status` attribute. Once True, set it back to False to reset.

.. code:: python

    if rtc.alarm_status:
        print("wake up!")
        rtc.alarm_status = False

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/pcf8563/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_PCF8563/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
