from PyQt5.QtCore import Qt, QPoint, QLine, QRectF, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPalette, QPen, \
    QPolygon, QPainterPath, QImage
from PyQt5.QtWidgets import QWidget
from math import trunc
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


class QTimeLineInstance:
    def __init__(self, duration, icon_path, index):
        self.__duration = duration
        color = QColor(Qt.lightGray)
        self.color = color
        self.defColor = color
        self.icon = QImage(icon_path) if icon_path else None
        self.startPos = 0
        self.endPos = self.__duration
        self.index = None

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, duration):
        self.__duration = duration
        self.endPos = self.__duration


class QTimeLine(QWidget):
    positionChanged = pyqtSignal(int)
    durationChanged = pyqtSignal(int)
    videoPositionChanged = pyqtSignal(int)
    selectedInstancesValueChanged = pyqtSignal(list)

    def __init__(self):
        super(QWidget, self).__init__()
        self.duration = 0
        self.text_color = QColor("#bbbbbb")
        self.font = QFont("Decorative", 10)
        self.video_position = 0
        self.instances = []
        self.selectedInstances = []

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
        self.__draw_instances()
        self.__draw_time()
        self.__draw_line()
        self.__draw_dash_lines()

        self.__draw_cursor_line()
        self.__draw_pointer()
        self.__qp.end()

    def __draw_time(self):
        self.__qp.setPen(self.text_color)
        self.__qp.setFont(self.font)
        w = 0
        scale = self.get_scale(self.duration)
        while w <= self.width():
            self.__qp.drawText(w - 50, 0, 100, 100, Qt.AlignHCenter,
                        hhmmss(self.duration * 1000 * w / self.width()))
            w += 100

    def __draw_line(self):
        self.__qp.setPen(QPen(Qt.darkCyan))
        self.__qp.drawLine(0, 40, self.width(), 40)

    def __draw_dash_lines(self):
        point = 0
        self.__qp.setPen(QPen(self.text_color))
        self.__qp.drawLine(0, 40, self.width(), 40)
        while point <= self.width():
            if point % 30 != 0:
                self.__qp.drawLine(3 * point, 40, 3 * point, 30)
            else:
                self.__qp.drawLine(3 * point, 40, 3 * point, 20)
            point += 10

    def __draw_instances(self):
        scale = self.get_scale(self.duration)
        current_duration = 0
        height = 50
        border = 5
        num = 1
        for instance in self.instances:
            path = QPainterPath()
            self.__qp.setPen(QPen(QColor("#EE7674")))
            x = instance.duration / scale
            path.addRect(
                QRectF(current_duration / scale, height - border/2,
                       x, height + border))

            self.__qp.fillPath(path, instance.color)
            self.__qp.drawPath(path)
            if instance.icon:
                overlay = instance.icon
                overlay = overlay.scaled(
                    int(instance.duration / scale), 50, Qt.KeepAspectRatio)
                self.__qp.drawImage(
                    QRectF(current_duration / scale, 50, overlay.width(), 50),
                    overlay)
            num += 1
            instance.startPos = current_duration / scale
            instance.endPos = (current_duration + instance.duration) / scale
            current_duration += instance.duration

    def __draw_cursor_line(self):
        if self.pos is not None \
                and self.width() >= self.pos.x() >= 0 \
                and self.is_in:
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

    def update_timeline(self, timeline_collection, icon_path = None, index = None):
        if len(timeline_collection) > len(self.instances):
            self.add_instance(timeline_collection[-1].duration, icon_path)
        elif len(timeline_collection) < len(self.instances):
            self.remove_instance(index)
        else:
            self.instances[index].duration =\
                timeline_collection[index].duration
            self.instances[index].icon =\
                QImage(icon_path) if icon_path else None
        self.update()

    def add_instance(self, duration, icon_path):
        self.instances.append(
            QTimeLineInstance(duration, icon_path, len(self.instances)))
        self.set_duration(self.duration + duration)

    def remove_instance(self, index):
        if index > 0:
            for instance in range(index, len(self.instances)):
                self.instances[instance].index -= 1
        self.set_duration(self.duration - self.instances[index].duration)
        self.instances.pop(index)

    def mouseMoveEvent(self, e):
        if 0 <= e.pos().x() <= self.width():
            self.pos = e.pos()

        # if mouse is being pressed, update pointer
        if self.clicking:
            x = self.pos.x()
            self.pointerPos = x
            self.positionChanged.emit(x)
            self.check_selection(e.pos().x(), e.pos().y())
            self.set_video_position(int(self.pointerPos * self.get_scale(self.duration * 1000)))
            self.pointerTimePos = self.pointerPos

        self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            x = e.pos().x()
            self.pointerPos = x
            self.positionChanged.emit(x)
            self.pointerTimePos = self.pointerPos
            self.set_video_position(int(self.pointerPos * self.get_scale(self.duration * 1000)))

            self.check_selection(e.pos().x(), e.pos().y())

            self.update()
            self.clicking = True  # Set clicking check to true

        if e.button() == Qt.RightButton:
            x = e.pos().x()
            self.check_selection(e.pos().x(), e.pos().y())
            self.update()
            self.clicking = True  # Set clicking check to true

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicking = False
        if e.button() == Qt.RightButton:
            self.clicking = False

    def enterEvent(self, e):
        self.is_in = True

    # Leave
    def leaveEvent(self, e):
        self.is_in = False
        self.update()

    def check_selection(self, x, y):
        found = False
        for instance in self.instances:
            if instance.startPos < x < instance.endPos and 45 < y < 105:
                instance.color = Qt.darkGray
                self.selectedInstances.append(instance)
                found = True
            else:
                if instance not in self.selectedInstances:
                    instance.color = instance.defColor
        if not found:
            self.selectedInstances.clear()
            for instance in self.instances:
                instance.color = instance.defColor
            self.selectedInstancesValueChanged.emit(self.selectedInstances)
        else:
            print(self.selectedInstances)
            self.selectedInstancesValueChanged.emit(self.selectedInstances)

    def set_video_position(self, pos):
        self.video_position = pos
        self.videoPositionChanged.emit(pos)
        self.set_position(self.video_position / 1000)

    def set_duration(self, duration):
        self.duration = trunc(duration)
        self.durationChanged.emit(trunc(duration))
        self.update()

    def set_position(self, position):
        self.pointerPos = \
            position / self.get_scale(self.duration) \
            if self.duration != 0 else 0
        if self.pointerPos > self.width():
            self.pointerPos = self.width()
        self.pointerTimePos = self.pointerPos
        self.positionChanged.emit(position)
        self.update()

    def get_scale(self, scale):
        return float(scale) / float(self.width())
