from lib.bot import JustRobot


def run() -> None:
    Bot = JustRobot()

    Bot.load()

    Bot.run()


if __name__ == '__main__':
    run()
