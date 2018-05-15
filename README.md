huber
=====

Ethernet driver and command-line tool for Huber baths.

<p align="center">
  <img src="http://www.huber-online.com/images/product_img/group_3.06.jpg" />
</p>

Installation
============

```
pip install huber
```

If you don't like pip, you can also install from source:

```
git clone https://github.com/numat/huber.git
cd huber
python setup.py install
```

Usage
=====

### Command Line

For basic tasks, this driver includes a command-line interface. Read the help
for more.

```
huber --help
```

### Python

For more complex projects, use python to automate your workflow. *This
driver solely uses asynchronous Python ≥3.5.*

```python
import asyncio
from huber import Bath

async def print_state():
    print(await bath.get())

bath = Bath('192.168.1.100')  # Change the IP to match your bath
ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(print_state())
bath.close()
ioloop.close()
```

If the bath is communicating, this should print a dictionary of the form:

```python
{
    'fill': 0.0,               # Oil level, [0, 1]
    'internal': 23.49,         # Internal temperature, °C
    'maintenance': 338,        # Time until maintenance alarm, days
    'pressure': 0.0,           # Pump head pressure, mbar
    'setpoint': 20.0,          # Temperature setpoint, °C
    'status': {
        'circulating': False,  # True if device is circulating
        'controlling': False,  # True if temperature control is active
        'error': False,        # True if an uncleared error is present
        'pumping': False,      # True if pump is on
        'warning': False       # True if an uncleared warning is present
    }
}
```

The main `get` method strings together multiple TCP requests, and can take >0.5s
to run. If you don't want all the data, you should instead use the following:

```python
await get_setpoint()          # °C
await get_internal()          # °C
await get_pressure()          # mbar
await get_pump_speed()        # rpm, may not be enabled
await get_fill_level()        # [0, 1]
await get_next_maintenance()  # days
await get_status()            # boolean dictionary
```

You can also set the temperature setpoint and (if enabled) pump speed.

```python
await bath.set_setpoint(50)     # °C
await bath.set_pump_speed(100)  # rpm
```

Implementation
==============

This uses the PB method described in
[the manual](http://www.huber-online.com/download/manuals/Handbuch_Datenkommunikation_PB_en.pdf).
Note that this does not take advantage of the PB package commands, which would
cut down on the data transmission at the cost of extra bath configuration.
This also does not take advantage of the high-accuracy PB data transmission,
as its resolution is unnecessary in NuMat's current use case.
