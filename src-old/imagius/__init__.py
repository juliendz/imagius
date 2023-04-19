
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication
from imagius.constants import HUMAN_APP_NAME
from imagius.init import init_app_data_dir, init_app_db


def run(argv):
    init_app_data_dir()
    init_app_db()

    from imagius.log import LOGGER
    LOGGER.info(
        '======================================Imagius starting up=======================================')

    import imagius.settings
    settings.load_settings()

    from imagius.main_window import MainWindow

    app = QApplication(argv)
    app.setApplicationName(HUMAN_APP_NAME)
    w = MainWindow()

    # with open('styles/Aqua.qss', 'r') as stylesheet:
    #     qss = stylesheet.read()

    # w.setStyleSheet(qss)

    w.setWindowTitle('Imagius')
    w.showMaximized()

    return app.exec_()
