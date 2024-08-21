"""Test the driver correctly initializes and returns mocked data."""
import random
from json import loads
from unittest import mock

import pytest

from huber import command_line
from huber.mock import Bath

fixed_random = random.random()
fixed_choice = random.choice([False, True])


@pytest.fixture
def huber_driver():
    """Confirm the driver correctly initializes."""
    return Bath('fake ip')


@pytest.fixture
def expected_data():
    """Return the mocked data."""
    with mock.patch('random.random', return_value=fixed_random), \
         mock.patch('random.choice', return_value=fixed_choice):
        return {
            'on': False,  # Temperature control (+pump) active
            'temperature': {
                'bath': 23.49,                  # Internal (bath) temperature, °C
                'process': 22.71,               # Process temperature, °C
                'setpoint': 50                  # Temperature setpoint, °C
            },
            'pump': {
                'pressure': random.random() * 1000,    # Pump head pressure, mbar
                'speed': random.random() * 1000,       # Pump speed, rpm
                'setpoint': 500                # Pump speed setpoint, rpm
            },
            'status': {
                'circulating': random.choice([False, True]),  # True if device is circulating
                'controlling': random.choice([False, True]),  # True if temp control is active
                'error': False,                        # True if an uncleared error is present
                'pumping': random.choice([False, True]),      # True if pump is on
                'warning': False,                      # True if an uncleared warning exists
            },
            'fill': random.random(),             # Oil level, [0, 1]
            'maintenance': random.random() * 365,  # Time until maintenance alarm, days
        }


@pytest.mark.asyncio
async def test_get_data(huber_driver, expected_data):
    """Confirm that the driver returns correct values on get() calls."""
    with mock.patch('random.random', return_value=fixed_random), \
         mock.patch('random.choice', return_value=fixed_choice):
        assert expected_data == await huber_driver.get()


@mock.patch('huber.Bath', Bath)
def test_driver_cli(capsys, expected_data):
    """Confirm the commandline interface works."""
    with mock.patch('random.random', return_value=fixed_random), \
         mock.patch('random.choice', return_value=fixed_choice):
        command_line(['fakeip'])
        captured = loads(capsys.readouterr().out)
        assert expected_data == captured


@mock.patch('huber.Bath', Bath)
def test_driver_cli_setpoint(capsys, expected_data):
    """Confirm setting a setpoint via the commandline interface works."""
    with mock.patch('random.random', return_value=fixed_random), \
         mock.patch('random.choice', return_value=fixed_choice):
        command_line(['fakeip', '--set-setpoint', '1.23'])
        captured = loads(capsys.readouterr().out)
        expected_data['temperature']['setpoint'] = 1.23
        assert expected_data == captured
