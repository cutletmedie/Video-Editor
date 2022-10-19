import unittest
from unittest.mock import patch
import os
from modules.project import Project
from modules.file import FileTypes

path = os.getcwd()
prev_tests_dir = path.split("\\tests")[0]
tests_dir = prev_tests_dir + '\\tests'
sources_dir = tests_dir + '\\sources\\'


class TestProject(unittest.TestCase):
    def setUp(self):
        self.project = Project()

    def tearDown(self) -> None:
        pass

    def test_init(self):
        self.assertEqual(self.project.timeline.collection, [])
        self.assertEqual(self.project.explorer.collection, [])

    def test_open_file(self):
        self.project.open_file(sources_dir + 'video.mp4')
        self.assertEqual(len(self.project.explorer.collection), 1)
        self.assertEqual(len(self.project.timeline.collection), 0)
        self.assertEqual(self.project.explorer.collection[0].file.path,
                         sources_dir + 'video.mp4')
        self.assertEqual(self.project.explorer.collection[0].file.file_type,
                         FileTypes.VIDEO)
        previous_element = self.project.explorer.collection[0].file
        previous_path = self.project.explorer.collection[0].file.path
        self.project.open_file(sources_dir + 'video.mp4')
        new_element = self.project.explorer.collection[0].file
        new_path = self.project.explorer.collection[0].file.path
        self.assertEqual(previous_path, new_path)
        self.assertNotEqual(previous_element, new_element)

        with open(sources_dir + "\\{}".format("text.txt"),
                  'w', encoding="utf-8") as file:
            file.write("test")
            file.close()

        self.project.open_file(sources_dir + 'text.txt')
        self.assertEqual(len(self.project.explorer.collection), 1)
        os.remove(sources_dir + "\\{}".format("text.txt"))

    answers = ['yes', 'no', 'close']

    @patch('builtins.input', side_effect=answers)
    def test_close_file(self, mock_input):
        self.project.open_file(sources_dir + 'video.mp4')
        self.assertEqual(len(self.project.explorer.collection), 1)
        self.assertEqual(len(self.project.timeline.collection), 0)
        self.assertEqual(self.project.explorer.collection[0].file.path,
                         sources_dir + 'video.mp4')
        self.project.close_file(self.project.explorer.collection[0])
        self.assertEqual(len(self.project.explorer.collection),
                         len(self.project.timeline.collection),
                         0)
        self.project.open_file(sources_dir + 'video.mp4')
        self.project.timeline.add_instance(
            self.project.explorer.collection[0])
        self.assertEqual(len(self.project.explorer.collection),
                         len(self.project.timeline.collection),
                         1)
        self.project.close_file(self.project.explorer.collection[0])
        self.assertEqual(len(self.project.explorer.collection),
                         len(self.project.timeline.collection),
                         0)
        self.project.open_file(sources_dir + 'video.mp4')
        self.project.timeline.add_instance(
            self.project.explorer.collection[0])
        self.project.close_file(self.project.explorer.collection[0])
        self.assertEqual(len(self.project.explorer.collection), 1)
        self.assertEqual(len(self.project.timeline.collection), 1)


