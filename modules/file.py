import os
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip
from enum import Enum


class FileTypes(Enum):
    VIDEO = 'video'
    AUDIO = 'audio'
    IMAGE = 'image'


extension_dict = {
    '.mp4': FileTypes.VIDEO,
    '.avi': FileTypes.VIDEO,
    '.mov': FileTypes.VIDEO,
    '.mp3': FileTypes.AUDIO,
    '.wav': FileTypes.AUDIO,
    '.jpg': FileTypes.IMAGE,
    '.png': FileTypes.IMAGE,
    '.jpeg': FileTypes.IMAGE
}


def get_file_type(file_path):
    file_extension = os.path.splitext(file_path)[1]
    if file_extension in extension_dict:
        return extension_dict[file_extension]
    else:
        return 'unknown'


class File:
    def __init__(self, file_path):
        self.__path = os.path.abspath(file_path)
        self.__file_type = get_file_type(self.__path)
        if self.__file_type == FileTypes.VIDEO:
            self.__content = VideoFileClip(self.__path)
        elif self.__file_type == FileTypes.AUDIO:
            self.__content = AudioFileClip(self.__path)
        elif self.__file_type == FileTypes.IMAGE:
            self.__content = ImageClip(self.__path)

    @property
    def path(self):
        return self.__path

    @property
    def file_type(self):
        return self.__file_type

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, new_content):
        self.__content = new_content
