"""Import shorthand and command-line tool for Huber baths."""

from huber.driver import Bath


def command_line(args=None):
    """Command-line interface to the Huber bath."""
    import argparse
    import asyncio
    import json
    parser = argparse.ArgumentParser(description="Control a Huber bath "
                                     "from the command line.")
    parser.add_argument('ip', help="The bath IP address.")
    parser.add_argument('--set-setpoint', '-s', default=None, type=float,
                        help="Sets the bath temperature setpoint.")
    args = parser.parse_args(args)

    async def print_state():
        async with Bath(args.ip) as bath:
            if args.set_setpoint is not None:
                await bath.set_setpoint(args.set_setpoint)
            print(json.dumps(await bath.get(), indent=4, sort_keys=True))

    asyncio.run(print_state())


if __name__ == '__main__':
    command_line()
