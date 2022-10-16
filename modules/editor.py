from moviepy.editor import *
import os


class Video:
    def __init__(self, name):
        self.video = VideoFileClip(name)

    def volume(self, n):
        self.video = self.video.volumex(n)

    def video_speed(self, n):
        self.video = self.video.fx(vfx.speedx, n)

    def crop(self, start=None, end=None):
        if not start:
            start = 0
        if not end:
            end = self.video.duration
        self.video = self.video.subclip(start, end)

    def export(self, name, path=None):
        if not path:
            path = os.getcwd() + '/export/'
            try:
                os.mkdir(path)
            except FileExistsError:
                pass
        path += name + '.mp4'
        self.video.write_videofile(path, fps=30)


class VideoFragment:
