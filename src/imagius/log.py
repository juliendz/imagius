import logging

LOGGER = logging.getLogger('imagius')
LOGGER.setLevel(logging.DEBUG)

LOG_FILE_HANDLER = logging.FileHandler('imagius.log')
LOG_FILE_HANDLER.setLevel(logging.DEBUG)

LOG_FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
LOG_FILE_HANDLER.setFormatter(LOG_FORMATTER)

LOGGER.addHandler(LOG_FILE_HANDLER)
