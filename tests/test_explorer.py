import unittest
import os
from modules.explorer import Explorer
from modules.file import File
from modules.timeline import TimelineInstance


path = os.getcwd()
os.chdir(path.replace('\\', '/').split("/tests")[0])
tests_dir = os.getcwd() + '/tests'
sources_dir = tests_dir + '/sources/'
os.chdir(path)
test_file = File(sources_dir + 'video.mp4')


class TestExplorer(unittest.TestCase):
    def setUp(self):
        self.explorer = Explorer()
        self.explorer.add_item(test_file)

    def tearDown(self) -> None:
        pass

    def test_init(self):
        self.explorer_init = Explorer()
        self.assertEqual(self.explorer_init.collection, [])

    def test_add_item(self):
        new_explorer = Explorer()
        new_explorer.add_item(test_file)
        self.assertEqual(new_explorer.collection[0].file, test_file)
        self.assertEqual(len(new_explorer.collection), 1)

    def test_remove_item(self):
        self.explorer.remove_item(self.explorer.collection[0])
        self.assertEqual(len(self.explorer.collection), 0)

    def test_get_instance(self):
        instance = TimelineInstance(self.explorer.collection[0])
        self.assertEqual(instance.file.path,
                         self.explorer.collection[0].file.path)
        self.assertEqual(instance.file.file_type,
                         self.explorer.collection[0].file.file_type)
        self.assertNotEqual(instance.file,
                         self.explorer.collection[0].file)
        self.assertNotEqual(instance.file.content,
                         self.explorer.collection[0].file.content)
        self.assertNotEqual(instance,
                            self.explorer.collection[0])
        self.assertEqual(instance.parent,
                            self.explorer.collection[0])
