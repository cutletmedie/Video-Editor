import copy


class ExplorerElement:
    def __init__(self, file):
        self.file = file
        self.next_element = None


class Explorer:
    def __init__(self):
        self.collection = []
        self.head = None

    def add_item(self, item):
        new_element = ExplorerElement(item)
        found_element = self.is_in_explorer(self, new_element)
        if found_element:
            found_element.file = item
            del new_element
            return
        if self.head:
            self.head.next_element = new_element
        self.head = new_element
        self.collection.append(new_element)

    def remove_item(self, item):
        found_element = self.is_in_explorer(self, item)
        if found_element:
            index = self.collection.index(found_element)
            if index != 0:
                self.collection[index-1].next_element =\
                    self.collection[index].next_element
            self.collection.remove(found_element)
            del found_element
            del item
            return

    @staticmethod
    def get_instance(explorer_element):
        """
        explorer_element, как ни странно, это ExplorerElement,
        instance возвращается в timeline
        и становится самостоятельным элементом
        """
        file = copy.copy(explorer_element.file)
        return file

    def get_explorer_element(self, path):
        '''
        :param path: str
        :return: ExplorerElement
        '''
        for element in self.collection:
            if element.file.path == path:
                return element

    @staticmethod
    def is_in_explorer(self, item):
        """
        Принимает File или ExplorerElement,
        возвращает ExplorerElement из коллекции,
        если у файла и элемента совпадают пути до файла
        """
        # if isinstance(item, str):
        #     for explorer_element in self.collection:
        #         if explorer_element.file.path == item:
        #             return True
        #     return False

        if isinstance(item, ExplorerElement):
            item = item.file
        for explorer_element in self.collection:
            if explorer_element.file.path == item.path:
                return explorer_element
