import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from moviepy.editor import *


class Window(QMainWindow):
    """Основное окно"""
    def __init__(self, full_filename=None):
        super(Window, self).__init__()
        self.initUI()

    def resizeEvent(self, e):
        super(Window, self).resizeEvent(e)
        self.preview_widget.setFixedSize(int(self.size().width() / 1.7),
                                         int(self.size().height() / 1.7))
        self.preview_group.setFixedSize(int(self.size().width() / 1.6),
                                        int(self.size().height() / 1.6))
        self.__explorer.setFixedHeight(int(self.height() / 2))
        # self.__explorer.setFixedSize(int(self.size().width() / 3.5), self.preview_group.height())

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
        self.init_preview()
        self.init_player()
        self.init_preview_controls()
        self.init_timeline()
        self.__inner_left_layout.addWidget(self.__explorer)
        self.__inner_left_layout.addWidget(self.__explorer_controls)
        self.__inner_right_layout.addWidget(
            self.preview_group)
        self.__inner_right_layout.addWidget(
            self.__preview_controls)
        self.__inner_right_layout.addWidget(self.__timeline)
        self.__main_layout.addLayout(self.__inner_left_layout)
        self.__main_layout.addLayout(self.__inner_right_layout)

    def init_explorer(self):
        self.__explorer = QTreeView()
        self.__explorer.setStyleSheet("""
            background-color: #3c3f41;
            color: #bbbbbb;
            font-size: 14px;
            border: 1px solid red;
            """)

    def init_explorer_controls(self):
        self.__explorer_controls = QGroupBox()
        frame = QFrame()
        frame.setStyleSheet("""
            background-color: #323232;
            color: #bbbbbb;
            font-size: 14px;
            border: 1px solid #323232;
            margin: 0px; padding: 10px;
            """)
        button = QPushButton()
        button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        # button.setFixedSize()
        layout = QHBoxLayout()
        layout.addWidget(frame)
        self.__explorer_controls.setStyleSheet("""
        [class="QGroupBox"] {
                    background-color: #3c3f41;
                    color: #bbbbbb;
                    font-size: 14px;
                    border: 1px solid red;
                    padding: 0px;}
                    """)
        self.__explorer_controls.setLayout(layout)

    def init_controls(self):
        self.__controls = QGroupBox()
        self.__controls.setStyleSheet("""
                    background-color: #3c3f41;
                    margin: 0px; padding: 0px;
                    border: 1px solid #323232;
                    """)

    def init_preview(self):
        self.preview_group = QGroupBox()
        self.preview_group.setStyleSheet("""
                   border: 1px solid #323232; 
                   border-radius: 1px; 
                   background-color: #323232;
                   """)
        preview_layout = QVBoxLayout()
        self.preview_widget = QVideoWidget()
        preview_layout.addWidget(self.preview_widget, 0, Qt.AlignCenter)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        self.preview_group.setLayout(preview_layout)

    def init_player(self):
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.setPosition(0)
        self.player.setVideoOutput(self.preview_widget)
        opening = QMediaContent(QUrl.fromLocalFile(
            "C:\\Users\\sjkey\\Downloads\\videoplayback.webm"))
        test_video = QMediaContent(
            QUrl.fromLocalFile(
                "C:\\Users\\sjkey\\Desktop\\ФТ\\repos\\Video-Editor\\tests\\sources\\video.mp4"))
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

    def init_preview_controls(self):
        buttons_size = QSize(40, 40)
        buttons_padding = 10

        def media_state_changed():
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.pause()
                self.play_button.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))
            else:
                self.player.play()
                self.play_button.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))


        self.__preview_controls = QGroupBox()
        self.__preview_controls.setStyleSheet("""
            [class="QGroupBox"] {
            border: 1px solid #323232;}
            [class="QPushButton"]""" +
            f"{{padding: {buttons_padding}px; }}")
        self.__preview_controls.setFixedHeight(buttons_size.height() + 2 * buttons_padding)
        preview_controls_layout = QHBoxLayout()
        preview_controls_layout.setSpacing(5)
        preview_controls_layout.setContentsMargins(0, 0, 0, 0)
        preview_controls_layout.setStretch(0, 0)
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
        self.__timeline = QGroupBox()
        self.__timeline.setStyleSheet("""
            background-color: #3c3f41;
            color: #bbbbbb;
            font-size: 14px;
            border: 1px solid #323232;
            """)
        # self.__timeline.setFixedHeight()


def main():
    """Точка входа в приложение"""
    app = QApplication(sys.argv)
    args = sys.argv
    window = Window(args[1] if len(args) > 1 else None)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
