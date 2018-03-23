from PyQt5 import QtCore
import logging
roaming_dir_path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppDataLocation)
log_name = 'imagius.log'

LOGGER = logging.getLogger('imagius')
LOGGER.setLevel(logging.DEBUG)

print()
LOG_FILE_HANDLER = logging.FileHandler('%s/imagius/%s' % (roaming_dir_path, log_name))
LOG_FILE_HANDLER.setLevel(logging.DEBUG)

LOG_FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
LOG_FILE_HANDLER.setFormatter(LOG_FORMATTER)

LOGGER.addHandler(LOG_FILE_HANDLER)
