from PyQt5.QtCore import Qt, QPoint, QLine, QRectF, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPalette, QPen, QPolygon, QPainterPath
from PyQt5.QtWidgets import QWidget
from random import randint

__textColor__ = QColor(187, 187, 187)
__backgroundColor__ = QColor(60, 63, 65)
__font__ = QFont('Decorative', 10)
__colors__ = [QColor(242, 158, 145), QColor(242, 195, 145), QColor(241, 242, 145), QColor(168, 242, 145),
              QColor(145, 242, 221), QColor(145, 179, 242), QColor(173, 145, 242), QColor(242, 145, 242)]


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
        self.textColor = QColor("#bbbbbb")
        self.font = QFont("Decorative", 10)
        self.pos = None
        self.pointerPos = None
        self.pointerTimePos = None
        self.clicking = False
        self.is_in = False

        self.setMouseTracking(True)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(self.textColor)
        qp.setFont(self.font)
        qp.setRenderHint(QPainter.Antialiasing)
        w = 0

        # Draw time
        scale = self.get_scale()
        while w <= self.width():
            qp.drawText(w - 50, 0, 100, 100, Qt.AlignHCenter,
                        hhmmss(w * scale))
            w += 100

        # Draw down line
        qp.setPen(QPen(Qt.darkCyan, 5, Qt.SolidLine))
        qp.drawLine(0, 40, self.width(), 40)

        # Draw dash lines
        point = 0
        qp.setPen(QPen(self.textColor))
        qp.drawLine(0, 40, self.width(), 40)
        while point <= self.width():
            if point % 30 != 0:
                qp.drawLine(3 * point, 40, 3 * point, 30)
            else:
                qp.drawLine(3 * point, 40, 3 * point, 20)
            point += 10

        if self.pos is not None and self.width() >= self.pos.x() >= 0 and self.is_in:
            qp.drawLine(self.pos.x(), 0, self.pos.x(), 40)

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
        qp.setClipPath(path)

        # Draw pointer
        qp.setPen(Qt.darkCyan)
        qp.setBrush(QBrush(Qt.darkCyan))

        qp.drawPolygon(poly)
        qp.drawLine(line)
        qp.end()

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

    def get_scale(self):
        return float(self.duration) / float(self.width())