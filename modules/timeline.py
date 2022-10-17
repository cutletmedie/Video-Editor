from modules.explorer import Explorer


class VideoInstance:
    def __init__(self, video):
        self.video = Explorer.get_instance(video)
        self.previous_video_instance = None
        self.next_video_instance = None


class Timeline:
    def __init__(self):
        self.head = None
        self.collection = []

    def add_instance(self, explorer, item, position=None):
        if item in explorer.collection:
            instance = VideoInstance(item)
            if position is None or position == len(self.collection):
                instance.previous_video_instance = self.head
                self.head = instance
                self.collection.append(instance)
            elif position == 0:
                instance.next_video_instance = self.collection[0]
                self.collection[0].previous_video_instance = instance
                self.collection.insert(position, instance)
            else:
                instance.previous_video_instance = \
                    self.collection[position - 1]
                instance.next_video_instance = self.collection[position]
                self.collection[position - 1].next_video_instance = instance
                self.collection[position].previous_video_instance = instance
                self.collection.insert(position, instance)
