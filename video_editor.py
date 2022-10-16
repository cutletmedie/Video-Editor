import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from moviepy.editor import *
from modules.editor import Video as video


class Window(QMainWindow):
    """Основное окно"""
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
    # video_clip = video('tests\\sources\\video.mp4')
    # video_clip.volume(0.5)
    # # video = CompositeVideoClip([video_clip])
    # video_clip.export('video')
    print("1234".split('5')[0])
    main()
