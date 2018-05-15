"""Import shorthand and command-line tool for Huber baths."""
from huber.driver import Bath


def command_line():
    """Command-line interface to the Huber bath."""
    import argparse
    import asyncio
    import json

    parser = argparse.ArgumentParser(description="Control a Huber bath "
                                     "from the command line.")
    parser.add_argument('ip', help="The bath IP address.")
    parser.add_argument('--set-setpoint', '-s', default=None, type=float,
                        help="Sets the bath temperature setpoint.")
    args = parser.parse_args()

    async def print_state():
        if args.set_setpoint is not None:
            await bath.set_setpoint(args.set_setpoint)
        print(json.dumps(await bath.get(), indent=4, sort_keys=True))

    bath = Bath(args.ip)
    ioloop = asyncio.get_event_loop()
    try:
        ioloop.run_until_complete(print_state())
    except KeyboardInterrupt:
        pass
    bath.close()
    ioloop.close()


if __name__ == '__main__':
    command_line()
