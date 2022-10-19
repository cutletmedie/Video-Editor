import os
from modules.timeline import Timeline
from modules.explorer import Explorer
from modules.file import File


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



    # def open_file(self, path):
    #     if os.path.isfile(path):
    #         replaced_files = self.explorer.add_item(video(os.path.abspath(path)))
    #         if replaced_files:
    #             for file in replaced_files:
    #                 if file.element.path ==
    #     else:
    #         raise FileNotFoundError

    # def close_file(self, path):
    #     path = os.path.abspath(path)
    #     for explorer_element in self.explorer.collection:
    #         explorer_element.element.path ==
    #     # for timeline_instance in self.timeline.collection:

