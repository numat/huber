"""Test the driver correctly initializes and returns mocked data."""
from unittest import mock

import random
import pytest

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
    with mock.patch('random.random', lambda: fixed_random), \
         mock.patch('random.choice', lambda arg: fixed_choice):
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
                'maintenance': random.random()*365,  # Time until maintenance alarm, days
            }


@pytest.mark.asyncio
async def test_get_data(huber_driver, expected_data):
    """Confirm that the driver returns correct values on get() calls."""
    with mock.patch('random.random', lambda: fixed_random), \
         mock.patch('random.choice', lambda arg: fixed_choice):
        assert expected_data == await huber_driver.get()
