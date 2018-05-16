"""Utility functions to handle Huber's number encoding."""


def int_to_hex(number, bits=16):
    """Convert int to a four-character hex string.

    This uses two's complement in encoding the integer, per Huber's
    manual.
    """
    return '{:04X}'.format((number + (1 << bits)) % (1 << bits))


def hex_to_int(hex_string, bits=16):
    """Convert a four-character hex string to an integer.

    This uses two's complement in decoding the hex string, per Huber's
    manual. This also manages the value '7fff' (32767), which is
    Huber's version of a command-not-implemented error.
    """
    number = int(hex_string, bits)
    if number == 32767:
        raise IOError("Command not enabled on this Huber model.")
    if number >> (bits - 1) == 1:
        number -= (1 << bits)
    return number


def parse(number, settings):
    """Parse a number according to formats from Huber's manual."""
    if number is None:
        return None
    format = settings['format']
    if format == 'd':
        return number
    elif format == 'f':
        return number / 100.0
    elif format == '%':
        return number / 1000.0
    elif format == 'list':
        return {v: bool(number >> i & 1) for i, v in settings['list'].items()}
    else:
        raise NotImplementedError(f'Number format "{format}" not supported.')


fields = {
    'setpoint': {
        'address': 0x00,
        'writable': True,
        'format': 'f',
        'range': (-151, 327)
    },
    'internal': {
        'address': 0x01,
        'format': 'f',
        'range': (-151, 327)
    },
    'pressure': {
        'address': 0x03,
        'format': 'f',
        'range': (0, 320)
    },
    'speed': {
        'address': 0x42,
        'writable': True,
        'format': 'd',
        'range': (0, 32000)
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
    }
}
