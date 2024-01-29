import os
from logging import getLogger, DEBUG, Formatter, FileHandler


class Logger:
    log_folder = "./logs"
    log_level = DEBUG
    formatter = Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    @classmethod
    def setup_logger(cls, name):
        if not os.path.exists(cls.log_folder):
            os.makedirs(cls.log_folder)

        logger = getLogger(name)
        logger.setLevel(cls.log_level)

        log_path = os.path.join(cls.log_folder, f"{name}.log")
        file_handler = FileHandler(log_path, encoding="UTF-8")
        file_handler.setFormatter(cls.formatter)
        logger.addHandler(file_handler)

        return logger
