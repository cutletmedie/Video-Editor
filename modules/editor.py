from moviepy.editor import *
from modules.changes_history import Actions
import os
import copy


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
            file_path = os.path.split(
                os.path.abspath(__file__))[0].replace('\\', '/')
            file_path = file_path[0:file_path.rfind('/')]
            path = file_path + '/export/'
            try:
                os.mkdir(path)
            except FileExistsError:
                pass
        path += name + '.mp4'
        self.video.write_videofile(path, fps=30)


class VideoFragment:
    def __init__(self, *videos):
        self.__content = []
        self.__duration = 0
        for video in videos:
            self.add_video(video)

    @property
    def content(self):
        return self.__content

    @property
    def duration(self):
        return self.__duration

    def add_video(self, video):
        self.__content.append(copy.copy(video))
        self.__duration += video.video.duration

    def remove_video(self, video):
        self.__content.remove(video)
        self.__duration -= video.video.duration

    def change_fragment(self, action, **kwargs):
        for video in self.__content:
            if action == Actions.VOLUME:
                video.volume(kwargs['n'])
            elif action == Actions.SPEED:
                previous_duration = video.video.duration
                video.video_speed(kwargs['n'])
                new_duration = video.video.duration
                self.__duration += new_duration - previous_duration
            elif action == Actions.CROP:
                if video.video.duration >= kwargs['end']:
                    self.__duration -= \
                        video.video.duration - \
                        (kwargs['end'] - kwargs['start'])
                    video.crop(kwargs['start'], kwargs['end'])
            elif action == Actions.EXPORT:
                video.export(kwargs['name'], kwargs['path'])
            else:
                raise ValueError('Unknown action')
