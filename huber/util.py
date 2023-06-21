"""Utilities to handle Huber's encodings."""
import csv
import os

root = os.path.normpath(os.path.dirname(__file__))
with open(os.path.join(root, 'faults.csv'), encoding='utf8') as in_file:
    reader = csv.reader(in_file)
    next(reader)
    faults = {int(row[0]): {
        'code': int(row[0]),
        'type': row[1],
        'condition': row[2] if len(row) >= 3 else None,
        'recovery': row[3] if len(row) == 4 else None
    } for row in reader if row[0]}

fields = {
    'on': {
        'address': 0x14,
        'writable': True,
        'format': 'b',
        'range': (0, 1)
    },
    'temperature': {
        'setpoint': {
            'address': 0x00,
            'writable': True,
            'format': 'f',
            'range': (-151, 327)
        },
        'bath': {
            'address': 0x01,
            'format': 'f',
            'range': (-151, 327)
        },
        'process': {
            'address': 0x07,
            'format': 'f',
            'range': (-151, 327)
        }
    },
    'pump': {
        'pressure': {
            'address': 0x03,
            'format': 'f',
            'range': (0, 320)
        },
        'speed': {
            'address': 0x26,
            'format': 'd',
            'range': (0, 32000)
        },
        'setpoint': {
            'address': 0x48,
            'writable': True,
            'format': 'd',
            'range': (1500, 4500)
        }
    },
    'fill': {
        'address': 0x0f,
        'format': '%',
        'range': (-0.001, 1)
    },
    'maintenance': {
        'address': 0x5c,
        'format': 'd'
    },
    'status': {
        'address': 0x0a,
        'format': 'list',
        'list': {
            0: 'controlling',
            1: 'circulating',
            4: 'pumping',
            8: 'error',
            9: 'warning'
        }
    },
    'error': {
        'address': 0x05,
        'format': 'fault',
        'writable': True
    },
    'warning': {
        'address': 0x06,
        'format': 'fault',
        'writable': True
    }
}


def int_to_hex(number, bits=16):
    """Convert int to a four-character hex string.

    This uses two's complement in encoding the integer, per Huber's
    manual.
    """
    return f'{(number + (1 << bits)) % (1 << bits):04X}'


def hex_to_int(hex_string, bits=16):
    """Convert a four-character hex string to an integer.

    This uses two's complement in decoding the hex string, per Huber's
    manual. This also manages the value '7fff' (32767), which is
    Huber's version of a command-not-implemented error.
    """
    number = int(hex_string, bits)
    if number == 32767:
        raise OSError("Command not enabled on this Huber model.")
    if number >> (bits - 1) == 1:
        number -= (1 << bits)
    return number


def parse(number, settings):
    """Parse a number according to formats from Huber's manual."""
    if number is None:
        return None
    format = settings['format']
    if format == 'b':
        return bool(number)
    if format == 'd':
        return number
    elif format == 'f':
        return number / 100.0
    elif format == '%':
        return number / 1000.0
    elif format == 'list':
        return {v: bool(number >> i & 1) for i, v in settings['list'].items()}
    elif format == 'fault':
        return faults[number] if number < 0 else None
    else:
        raise NotImplementedError(f'Number format "{format}" not supported.')


def get_field(key):
    """Search period-separated key searching on `fields`."""
    f = fields
    for k in key.split('.'):
        f = f[k]  # type: ignore
    return f


def set_nested(dictionary, keys, value):
    """Use period-separated keys to set nested dictionary value."""
    d = dictionary
    keys = keys.split('.')
    nodes, leaf = keys[:-1], keys[-1]
    for node in nodes:
        if node not in d:
            d[node] = {}
        d = d[node]
    d[leaf] = value
