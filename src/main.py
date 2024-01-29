from modules.logger import Logger


def main():
    logger = Logger.setup_logger("main")
    logger.info("Hello, world!")


if __name__ == "__main__":
    main()
