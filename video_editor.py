from modules import module
import os
import sys
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class Window(QMainWindow):
    """Main Window."""

    def __init__(self, full_filename=None):
        super(Window, self).__init__()


def main():
    """Точка входа в приложение"""
    app = QApplication(sys.argv)
    args = sys.argv
    window = Window(args[1] if len(args) > 1 else None)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
    # module.print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
