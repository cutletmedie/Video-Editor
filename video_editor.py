import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from moviepy.editor import *
from modules.editor import Video as video


class Window(QMainWindow):
    """Основное окно"""
    def __init__(self, full_filename=None):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.setWindowTitle('Видеоредактор')
        window_css = """
            background-color: #3c3f41; 
            color: #bbbbbb; 
            font-size: 14px;
            """
        self.setStyleSheet(window_css)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        central_widget = QWidget(self)
        outer_layout = QHBoxLayout()
        outer_layout.setSpacing(0)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        inner_right_layout = QVBoxLayout()
        inner_right_layout.setSpacing(0)
        inner_right_layout.setContentsMargins(0, 0, 0, 0)
        inner_left_layout = QVBoxLayout()
        inner_left_layout.setSpacing(0)
        inner_left_layout.setContentsMargins(0, 0, 0, 0)
        explorer = QGroupBox()
        explorer.setStyleSheet("margin: 0px; padding: 0px; border: 1px solid #323232; border-top: 0px;")

        video_group = QGroupBox()
        video_group.setStyleSheet("border: 1px solid #323232; border-radius: 1px; border-left: 0px; border-top: 0px;")
        video_layout = QVBoxLayout()
        self.widget = QVideoWidget(central_widget)
        self.widget.setFixedSize(int(self.size().width() / 2),
                                 int(self.size().height() / 2))
        video_layout.addWidget(self.widget)
        video_group.setLayout(video_layout)
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.setVideoOutput(self.widget)
        self.content = QMediaContent(QUrl.fromLocalFile("C:\\Users\\sjkey\\Desktop\\ФТ\\repos\\Video-Editor\\tests\\sources\\video.mp4"))
        self.player.setMedia(self.content)
        self.player.play()
        buttons_group = QGroupBox()
        play_button = QPushButton()
        play_button.setFixedSize(50, 50)
        play_button.setStyleSheet("border-radius : {}px; border: 1px solid #323232;".format(int(play_button.size().width() / 2)))
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(play_button, alignment=Qt.AlignCenter)
        buttons_group.setLayout(buttons_layout)

        inner_left_layout.addWidget(explorer)
        inner_right_layout.addWidget(video_group)
        inner_right_layout.addWidget(buttons_group)

        outer_layout.addLayout(inner_left_layout)
        outer_layout.addLayout(inner_right_layout)
        central_widget.setLayout(outer_layout)
        self.setCentralWidget(central_widget)

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


def main():
    """Точка входа в приложение"""
    app = QApplication(sys.argv)
    args = sys.argv
    window = Window(args[1] if len(args) > 1 else None)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
