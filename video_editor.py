import os
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from modules.qtimeline import QTimeLine, hhmmss
from modules.project import Project
from modules.temp_directory import temp_dir, create_temp_icon

class Window(QMainWindow):
    """Основное окно"""
    def __init__(self):
        super(Window, self).__init__()
        self.project = Project()
        self.__grid_files = []
        self.initUI()

    def resizeEvent(self, e):
        super(Window, self).resizeEvent(e)
        self.slider.setFixedHeight(int(self.preview_group.height() * 0.05))
        self.preview_widget.setFixedSize(
            int(self.size().width() / 1.7),
            int(self.size().height() / 1.7))
        self.preview_group.setFixedSize(
            int(self.size().width() / 1.6),
            int(self.size().height() / 1.6 + self.slider.height()))
        self.slider.setFixedWidth(
            int(self.preview_group.width() -
                self.preview_group.width() * 0.25))

        self.explorer_grid_widget.setFixedSize( int(self.width() - self.preview_group.width()),int(self.height() / 2))

    def initUI(self):
        self.resize(1280, 720)
        self.setWindowTitle('Видеоредактор')
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        window_css = """
            background-color: #3c3f41; 
            color: #bbbbbb; 
            font-size: 14px;
            """
        self.setStyleSheet(window_css)
        self.init_menubar()
        self.setMinimumSize(1280, 720)
        # self.setFixedSize(self.size())
        # self.setWindowFlags(Qt.WindowMinimizeButtonHint
        # | Qt.WindowCloseButtonHint)

        self.__central_widget = QWidget(self)
        self.concatenate_inner_layouts()

        self.__central_widget.setLayout(self.__main_layout)
        self.setCentralWidget(self.__central_widget)

    def init_menubar(self):
        menu_bar = self.menuBar()
        menu_css = """
            background-color: #3c3f41;
            color: #bbbbbb;
            font-size: 14px; 
            border-bottom: 1px solid #515151;
            """
        menu_bar.setStyleSheet(menu_css)
        file_menu = menu_bar.addMenu("&Файл")

    def init_inner_layouts(self):
        self.__main_layout = QHBoxLayout()
        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.__main_layout.setSpacing(0)
        self.__inner_right_layout = QVBoxLayout()
        self.__inner_left_layout = QVBoxLayout()

    def concatenate_inner_layouts(self):
        self.init_inner_layouts()
        self.init_explorer()
        self.init_explorer_controls()
        self.init_controls()
        self.init_player()
        self.init_preview()

        self.init_preview_controls()
        self.init_timeline()

        self.__inner_left_layout.addWidget(self.explorer_grid_widget)
        self.__inner_left_layout.addWidget(self.__explorer_controls)
        self.__inner_left_layout.addWidget(self.__controls)
        self.__inner_right_layout.addWidget(
            self.preview_group)
        self.__inner_right_layout.addWidget(
            self.__preview_controls)
        self.__inner_right_layout.addWidget(self.__timeline_widget)
        self.__main_layout.addLayout(self.__inner_left_layout)
        self.__main_layout.addLayout(self.__inner_right_layout)

    def init_explorer(self):
        self.explorer_grid_widget = QWidget(self)
        self.explorer_grid_widget.setStyleSheet(""" [class="QWidget"] {
            background-color: #3c3f41;
            color: #bbbbbb;
            font-size: 14px;
            border: 1px solid #323232;}
            [class="QLabel"] {
            background-color: #3c3f41;
            color: #1f1f1f;
            font-size: 14px;}
            """)
        self.explorer_grid = QGridLayout(self.explorer_grid_widget)
        self.fulfill_grid()

    def fulfill_grid(self):
        for i in range(5):
            for j in range(5):
                self.explorer_grid.addWidget(QLabel(), j, i)

    def init_explorer_controls(self):
        buttons_size = QSize(30, 30)
        buttons_padding = 5
        self.__explorer_controls = QGroupBox()
        self.__explorer_controls.setStyleSheet("""
                    [class="QGroupBox"] {
                    border: 1px solid #323232;}""" +
                    """[class="QPushButton"]""" +
                    f"""{{ font-size: 18px;
                    color: #1f1f1f;
                    title-align: center;
                    padding: {buttons_padding}px;
                    background-color: #515151;}}""")
        self.__explorer_controls.setFixedHeight(
            buttons_size.height() + 2 * buttons_padding)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(buttons_padding, 0, 0, 0)
        buttons_layout.setAlignment(Qt.AlignLeft)
        open_file_button = QPushButton("+")
        open_file_button.setFixedSize(buttons_size)
        open_file_button.clicked.connect(self.open_file)
        buttons_layout.addWidget(open_file_button)
        self.__explorer_controls.setLayout(buttons_layout)

    def init_controls(self):
        self.__controls = QGroupBox()
        self.__controls.setStyleSheet("""
                    background-color: #3c3f41;
                    margin: 0px; padding: 0px;
                    border: 1px solid #323232;
                    """)
        frame = QFrame()
        frame.setStyleSheet("""
                    background-color: #323232;
                    color: #bbbbbb;
                    font-size: 14px;
                    border: 1px solid #323232;
                    margin: 0px; padding: 10px;
                    """)
        layout = QHBoxLayout()
        layout.addWidget(frame)
        self.__controls.setLayout(layout)

    def init_player(self):
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.setPosition(0)

        opening = QMediaContent(QUrl.fromLocalFile(
            "C:\\Users\\sjkey\\Downloads\\Opening.webm"))
        test_video = QMediaContent(
            QUrl.fromLocalFile(
                "C:\\Users\\sjkey\\Desktop\\ФТ" +
                "\\repos\\Video-Editor\\tests\\sources\\video.mp4"))
        jojo = QMediaContent(
            QUrl.fromLocalFile(
                "C:\\Users\\sjkey\\Downloads\\U Got That - JJBA.mp4"))
        edit_wolves = QMediaContent(
            QUrl.fromLocalFile(
                "C:\\Users\\sjkey\\Downloads\\The Last Of Us │ Wolves.mp4"))
        edit_pet_cheetah = QMediaContent(QUrl.fromLocalFile(
            "C:\\Users\\sjkey\\Downloads\\Jinx 丨 Pet Cheetah.mp4"))
        self.playlist = QMediaPlaylist()
        self.playlist.addMedia([edit_wolves, edit_pet_cheetah, jojo, opening])
        self.player.setPlaylist(self.playlist)
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        lambda_set_video_position = \
            lambda: self.__timeline.set_video_position(self.player.position())
        self.player.positionChanged.connect(lambda_set_video_position)
        self.player.durationChanged.connect(self.update_duration)

    def init_preview(self):
        self.preview_group = QGroupBox()
        self.preview_group.setStyleSheet("""
                   border: 1px solid #323232; 
                   border-radius: 1px; 
                   background-color: #323232;
                   """)
        self.preview_group.setAlignment(Qt.AlignCenter)
        preview_layout = QVBoxLayout()
        self.preview_widget = QVideoWidget()
        preview_layout.addWidget(self.preview_widget, 1, Qt.AlignCenter)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_duration_layout = QHBoxLayout()
        self.current_TimeLabel = QLabel("00:00:00")
        self.current_TimeLabel.setStyleSheet("""
                      color: #bbbbbb;
                      """)
        self.total_TimeLabel = QLabel("00:00:00")
        self.total_TimeLabel.setStyleSheet("""
                      color: #bbbbbb;
                      """)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setStyleSheet("""
                    QSlider::groove:horizontal {
                    border: 1px solid #515151;
                    height: 10px;
                    background: #323232;
                    margin: 2px 0;
                    }
                    QSlider::handle:horizontal {
                    background: #bbbbbb;
                    border: 1px solid #5c5c5c;
                    width: 8px;
                    margin: -2px 0;
                    border-radius: 3px;
                    }
                    """)
        self.slider.valueChanged.connect(self.player.setPosition)
        preview_duration_layout.addWidget(
            self.current_TimeLabel, 0, Qt.AlignRight)
        preview_duration_layout.addWidget(self.slider)
        preview_duration_layout.addWidget(
            self.total_TimeLabel, 0, Qt.AlignLeft)
        preview_layout.addLayout(preview_duration_layout)
        self.preview_group.setLayout(preview_layout)
        self.player.setVideoOutput(self.preview_widget)

    def init_preview_controls(self):
        buttons_size = QSize(40, 40)
        buttons_padding = 5

        def media_state_changed():
            if self.player.mediaStatus() in (QMediaPlayer.NoMedia,
                                            QMediaPlayer.UnknownMediaStatus,
                                            QMediaPlayer.InvalidMedia):
                self.play_button.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))
                return
            if self.player.state() == QMediaPlayer.PlayingState:
                    self.player.pause()
                    self.play_button.setIcon(
                        self.style().standardIcon(QStyle.SP_MediaPlay))
            elif self.player.state() == QMediaPlayer.PausedState:
                self.player.play()
                self.play_button.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
            elif self.player.state() == QMediaPlayer.StoppedState:
                self.player.play()
                self.play_button.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))

        self.__preview_controls = QGroupBox()
        self.__preview_controls.setStyleSheet("""
            [class="QGroupBox"] {
            border: 1px solid #323232;}
            [class="QPushButton"]""" +
            f"{{padding: {buttons_padding}px; background-color: #515151;}}")
        self.__preview_controls.setFixedHeight(buttons_size.height() + 2 * buttons_padding)
        preview_controls_layout = QHBoxLayout()
        preview_controls_layout.setContentsMargins(0, 0, 0, 0)
        self.play_button = QPushButton()
        self.play_button.setFixedSize(buttons_size)
        media_state_changed()
        self.play_button.clicked.connect(media_state_changed)
        self.next_button = QPushButton()
        self.next_button.setFixedSize(buttons_size)
        self.next_button.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.next_button.clicked.connect(self.player.playlist().next)
        self.previous_button = QPushButton()
        self.previous_button.setFixedSize(buttons_size)
        self.previous_button.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.previous_button.clicked.connect(self.player.playlist().previous)
        preview_controls_layout.addWidget(
            self.previous_button, 0, Qt.AlignRight)
        preview_controls_layout.addWidget(
            self.play_button)
        preview_controls_layout.addWidget(
            self.next_button, 0, Qt.AlignLeft)
        self.__preview_controls.setLayout(preview_controls_layout)

    def init_timeline(self):
        self.__timeline_widget = QWidget()
        self.__timeline_widget.setStyleSheet("""
            background-color: #3c3f41;
            color: #bbbbbb;
            font-size: 14px;
            border: 1px solid #323232;
            """)
        timeline_layout = QHBoxLayout()
        self.__timeline = QTimeLine()
        timeline_layout.addWidget(self.__timeline)
        self.__timeline_widget.setLayout(timeline_layout)
        lambda_update_position = \
            lambda: self.update_position(self.__timeline.video_position)
        self.__timeline.videoPositionChanged.connect(lambda_update_position)

    def open_file(self):
        all_files = QFileDialog.getOpenFileNames(
            self, "Открыть файл", "",
            """Видеофайлы (*.mp4 *.MOV *.webm);;
            Аудиофайлы (*.mp3);;
            Изображения (*.jpeg *.jpg *.png)""")[0]
        for file_path in all_files:
            file_path = os.path.abspath(file_path)
            self.project.open_file(file_path)
            if len(self.__grid_files) < len(self.project.explorer.collection):
                for i in range(len(self.__grid_files), len(self.project.explorer.collection)):
                    self.add_icon(file_path)
                    self.__grid_files.append(file_path)

    def add_icon(self, file_path):
        icon_name = os.path.basename(file_path)
        icon_path = create_temp_icon(file_path)
        if icon_path:
            icon = QLabel()
            tip = icon_name
            icon.setToolTip(tip)
            icon.setAlignment(Qt.AlignCenter)
            icon.mouseDoubleClickEvent = \
                lambda event: self.add_instance_to_timeline(file_path)
            pixmap = QPixmap(icon_path)
            icon.setPixmap(pixmap.scaled(150, 100, Qt.KeepAspectRatio))

            row = len(self.__grid_files) // self.explorer_grid.columnCount()
            col = len(self.__grid_files) % self.explorer_grid.columnCount()
            self.explorer_grid.addWidget(icon, row, col)

    def update_position(self, position):
        if position >= 0:
            self.current_TimeLabel.setText(hhmmss(position))

        self.slider.blockSignals(True)
        self.__timeline.blockSignals(True)
        if self.player.position() != position:
            self.player.setPosition(position)
        # self.__timeline.video_position = self.player.position()
        # self.__timeline.set_position(self.player.position())
        self.slider.setValue(position)
        self.slider.blockSignals(False)
        self.__timeline.blockSignals(False)

    def update_duration(self, duration):
        self.slider.setMaximum(duration)
        if duration >= 0:
            self.total_TimeLabel.setText(hhmmss(duration))
            self.__timeline.set_duration(duration)

    def add_instance_to_timeline(self, file_path):
        self.project.add_instance_to_timeline(file_path)
        # self.update_timeline()


def main():
    """Точка входа в приложение"""
    os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = 'windowsmediafoundation'
    app = QApplication(sys.argv)
    args = sys.argv
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
