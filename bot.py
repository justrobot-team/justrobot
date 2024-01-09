from lib.bot import JustRobot


def main() -> None:
    Bot = JustRobot()

    Bot.load()

    Bot.run()


if __name__ == '__main__':
    main()
