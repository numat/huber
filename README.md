huber
=====

Ethernet driver and command-line tool for Huber baths.

<p align="center">
  <img src="https://www.huber-usa.com/fileadmin/_processed_/6/3/csm_Huber-Bad-Umwaelzthermostate-Gruppenbild_f3840bba75.png" />
</p>

Installation
============

```
pip install huber
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

async def get():
    async with Bath('192.168.1.100') as bath:
        print(await bath.get())

asyncio.run(get())
```

If the bath is communicating, this should print a dictionary of the form:

```python
{
    'on': False,               # Temperature control (+pump) active
    'temperature': {
        'bath': 23.49,         # Internal (bath) temperature, °C
        'setpoint': 20.0       # Temperature setpoint, °C
    },
    'pump': {
        'pressure': 0.0,       # Pump head pressure, mbar
        'speed': 0,            # Pump speed, rpm
        'setpoint': 0          # Pump speed setpoint, rpm
    },
    'status': {
        'circulating': False,  # True if device is circulating
        'controlling': False,  # True if temperature control is active
        'error': False,        # True if an uncleared error is present
        'pumping': False,      # True if pump is on
        'warning': False       # True if an uncleared warning is present
    },
    'fill': 0.0,               # Oil level, [0, 1]
    'maintenance': 338,        # Time until maintenance alarm, days
    'warning': {               # Only present if warning is detected
        'code': -1,
        'condition': '',
        'recovery': '',
        'type': ''
    },
    'error': {                 # Only present if error is detected
        'code': -1,
        'condition': '',
        'recovery': '',
        'type': ''
    }
}
```

The main `get` method strings together multiple TCP requests, and can take >0.5s
to run. If you don't want all the data, you should instead use the following:

```python
await bath.get_setpoint()             # °C
await bath.get_bath_temperature()     # °C
await bath.get_process_temperature()  # °C (optionally installed)
await bath.get_pressure()             # mbar
await bath.get_pump_speed()           # rpm
await bath.get_fill_level()           # [0, 1]
await bath.get_next_maintenance()     # days
await bath.get_status()               # boolean dictionary
await bath.get_warning()              # None or dictionary
await bath.get_error()                # None or dictionary
```

You can also start, stop, set temperature setpoint, and set pump speed.

```python
await bath.start()
await bath.stop()
await bath.set_setpoint(50)      # °C
await bath.set_pump_speed(2000)  # rpm
await bath.clear_warning()
await bath.clear_error()
```

Implementation
==============

This uses the PB method described in
[the manual](http://www.huber-online.com/download/manuals/Handbuch_Datenkommunikation_PB_en.pdf).
Note that this does not take advantage of the PB package commands, which would
cut down on the data transmission at the cost of extra bath configuration.
This also does not take advantage of the high-accuracy PB data transmission,
as its resolution is unnecessary in most use cases.
