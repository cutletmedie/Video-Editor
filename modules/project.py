import os
from modules.timeline import Timeline
from modules.explorer import Explorer
from modules.file import File
from modules.temp_directory import temp_dir


class Project:
    def __init__(self):
        self.explorer = Explorer()
        self.timeline = Timeline()

    def open_file(self, path):
        path = os.path.abspath(path)
        if os.path.isfile(path):
            file = File(path)
            if file.file_type == 'unknown':
                del file
                return
            self.explorer.add_item(file)

    def close_file(self, explorer_instance):
        select = []
        for instance in self.timeline.collection:
            if instance.parent is explorer_instance:
                select.append(self.timeline.collection[
                    self.timeline.collection.index(instance)])
        if select:
            answer = input("""Этот файл используется на таймлайне.\n
            Вы уверены, что хотите его закрыть? (y/n)""")
            answer = answer.lower()
            if answer in ['y', 'yes']:
                for item in select:
                    self.timeline.remove_instance(item)
                self.explorer.remove_item(explorer_instance)
            else:
                return
        else:
            self.explorer.remove_item(explorer_instance)

    def add_instance_to_timeline(self, path):
        explorer_element = self.explorer.get_explorer_element(path)
        self.timeline.add_instance(explorer_element)

    def remove_instance_from_timeline(self, index):
        instance = self.timeline.collection[index]
        self.timeline.remove_instance(instance)
