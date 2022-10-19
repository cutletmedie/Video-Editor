from modules.explorer import Explorer
import copy
from moviepy.editor import *


class TimelineInstance:
    def __init__(self, explorer_element):
        explorer_file = Explorer.get_instance(explorer_element)
        self.file = explorer_file
        self.file.content = self.file.content.subclip(
            0, self.file.content.duration)
        self.previous_instance = None
        self.next_instance = None
        self.__parent = explorer_element
        self.__volume_percentage = 100
        self.__speed_percentage = 100

    @property
    def parent(self):
        return self.__parent

    @property
    def volume_percentage(self):
        return self.__volume_percentage

    @property
    def speed_percentage(self):
        return self.__speed_percentage

    def change_volume(self, n):
        if n < 0.01 or n > 2:
            raise ValueError("Значение должно быть между 0.01 и 2")
        elif self.__volume_percentage != 100:
            self.file.content = self.file.content.volumex(
                100 / self.__volume_percentage)
            self.file.content = self.file.content.volumex(n)
            self.__volume_percentage = n * 100
        else:
            self.file.content = self.file.content.volumex(n)
            self.__volume_percentage = n * 100

    def change_speed(self, n):
        if n < 0.01 or n > 2:
            raise ValueError("Значение должно быть между 0.01 и 2")
        elif self.__speed_percentage != 100:
            self.file.content = self.file.content.speedx(
                100 / self.__speed_percentage)
            self.file.content = self.file.content.speedx(n)
            self.__speed_percentage = n * 100
        else:
            self.file.content = self.file.content.speedx(n)
            self.__speed_percentage = n * 100
    #
    # def crop(self, start=None, end=None):
    #     if not start:
    #         start = 0
    #     if not end:
    #         end = self.file.duration
    #     self.file = self.file.subclip(start, end)


class Timeline:
    def __init__(self):
        self.head = None
        self.collection = []

    def add_instance(self, explorer_element, position=None):
        new_instance = TimelineInstance(explorer_element)
        if position is None or position == len(self.collection):
            new_instance.previous_instance = self.head
            self.head = new_instance
            self.collection.append(new_instance)
        elif position == 0:
            new_instance.next_instance = self.collection[0]
            self.collection[0].previous_instance = new_instance
            self.collection.insert(position, new_instance)
        else:
            new_instance.previous_instance = \
                self.collection[position - 1]
            new_instance.next_instance = self.collection[position]
            self.collection[position - 1].next_instance = new_instance
            self.collection[position].previous_video_instance = new_instance
            self.collection.insert(position, new_instance)

    def remove_instance(self, instance):
        position = self.collection.index(instance)
        if position == len(self.collection) - 1:
            self.head.next_instance = None
            self.head = instance.previous_instance
            self.collection.remove(instance)
            del instance
            return
        elif position == 0:
            self.collection[1].previous_instance = None
            self.collection.remove(instance)
            del instance
            return
        else:
            self.collection[position - 1].next_instance = \
                self.collection[position + 1]
            self.collection[position + 1].previous_instance = \
                self.collection[position - 1]
            self.collection.remove(instance)
            del instance
            return
