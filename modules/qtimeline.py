from PyQt5.QtCore import Qt, QPoint, QLine, QRectF, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPalette, QPen, \
    QPolygon, QPainterPath
from PyQt5.QtWidgets import QWidget
from random import randint

__textColor__ = QColor(187, 187, 187)
__backgroundColor__ = QColor(60, 63, 65)
__font__ = QFont('Decorative', 10)
__colors__ = [QColor(242, 158, 145), QColor(242, 195, 145),
              QColor(241, 242, 145), QColor(168, 242, 145),
              QColor(145, 242, 221), QColor(145, 179, 242),
              QColor(173, 145, 242), QColor(242, 145, 242)]


def hhmmss(ms):
    #     # s = 1000
    #     # m = 60000
    #     # h = 3600000
    s = round(ms / 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


class QTimeLine(QWidget):
    positionChanged = pyqtSignal(int)
    durationChanged = pyqtSignal(int)

    def __init__(self, duration):
        super(QWidget, self).__init__()
        self.duration = duration
        self.text_color = QColor("#bbbbbb")
        self.font = QFont("Decorative", 10)
        self.pos = None
        self.pointerPos = None
        self.pointerTimePos = None
        self.clicking = False
        self.is_in = False
        self.__qp = QPainter()

        self.setMouseTracking(True)

    def paintEvent(self, event):
        self.__qp.begin(self)
        self.__qp.setRenderHint(QPainter.Antialiasing)
        self.__draw_time()
        self.__draw_line()
        self.__dash_lines()
        self.__draw_cursor_line()
        self.__draw_pointer()

    def __draw_time(self):
        self.__qp.setPen(self.text_color)
        self.__qp.setFont(self.font)
        w = 0
        scale = self.get_scale(self.duration)
        while w <= self.width():
            self.__qp.drawText(w - 50, 0, 100, 100, Qt.AlignHCenter,
                        hhmmss(w * scale))
            w += 100

    def __draw_line(self):
        self.__qp.setPen(QPen(Qt.darkCyan))
        self.__qp.drawLine(0, 40, self.width(), 40)

    def __dash_lines(self):
        point = 0
        self.__qp.setPen(QPen(self.text_color))
        self.__qp.drawLine(0, 40, self.width(), 40)
        while point <= self.width():
            if point % 30 != 0:
                self.__qp.drawLine(3 * point, 40, 3 * point, 30)
            else:
                self.__qp.drawLine(3 * point, 40, 3 * point, 20)
            point += 10

    def __draw_cursor_line(self):
        if self.pos is not None and self.width() >= self.pos.x() >= 0 and self.is_in:
            self.__qp.drawLine(self.pos.x(), 0, self.pos.x(), 40)

    def __draw_pointer(self):
        if self.pointerPos is not None:
            line = QLine(
                QPoint(int(self.pointerTimePos), 40),
                QPoint(int(self.pointerTimePos),
                       self.height()))
            poly = QPolygon(
                [QPoint(int(self.pointerTimePos) - 10, 20),
                 QPoint(int(self.pointerTimePos) + 10, 20),
                 QPoint(int(self.pointerTimePos), 40)])
        else:
            line = QLine(QPoint(0, 0), QPoint(0, self.height()))
            poly = QPolygon([QPoint(-10, 20), QPoint(10, 20), QPoint(0, 40)])

        path = QPainterPath()
        path.addRect(self.rect().x(), self.rect().y(), self.rect().width(),
                     self.rect().height())
        self.__qp.setClipPath(path)
        self.__qp.setPen(Qt.darkCyan)
        self.__qp.setBrush(QBrush(Qt.darkCyan))

        self.__qp.drawPolygon(poly)
        self.__qp.drawLine(line)
        self.__qp.end()

    def mouseMoveEvent(self, e):
        if 0 <= e.pos().x() <= self.width():
            self.pos = e.pos()

        # if mouse is being pressed, update pointer
        if self.clicking:
            x = self.pos.x()
            self.pointerPos = x
            self.positionChanged.emit(x)
            # self.check_selection(x)
            self.pointerTimePos = self.pointerPos

        self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            x = e.pos().x()
            self.pointerPos = x
            self.positionChanged.emit(x)
            self.pointerTimePos = self.pointerPos

            self.update()
            self.clicking = True  # Set clicking check to true

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicking = False  # Set clicking check to false

    def enterEvent(self, e):
        self.is_in = True

    # Leave
    def leaveEvent(self, e):
        self.is_in = False
        self.update()

    def set_duration(self, duration):
        self.duration = duration
        self.durationChanged.emit(duration)
        self.update()

    def set_position(self, pos):
        self.pointerPos = pos / self.get_scale(self.duration) \
            if self.duration != 0 else 0
        if self.pointerPos > self.width():
            self.pointerPos = self.width()
        self.pointerTimePos = self.pointerPos
        self.positionChanged.emit(pos)
        self.update()

    def get_scale(self, scale):
        return float(scale) / float(self.width())
