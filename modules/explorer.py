import copy


class Explorer:
    def __init__(self):
        self.collection = []

    def add_item(self, item):
        if item not in self.collection:
            self.collection.append(item)

    def remove_item(self, item):
        if item in self.collection:
            self.collection.remove(item)
            del item

    @staticmethod
    def get_instance(item):
        instance = copy.copy(item)
        return instance
