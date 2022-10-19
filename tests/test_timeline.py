import unittest
import os
from modules.timeline import Timeline, TimelineInstance
from modules.explorer import Explorer
from modules.file import File

path = os.getcwd()
os.chdir(path.replace('\\', '/').split("/tests")[0])
tests_dir = os.getcwd() + '/tests'
sources_dir = tests_dir + '/sources/'
os.chdir(path)
test_video = File(sources_dir + 'video.mp4')
explorer = Explorer()
explorer.add_item(test_video)


class TestTimeline(unittest.TestCase):
    def setUp(self):
        self.timeline = Timeline()
        self.timeline.add_instance(explorer.collection[0])

    def tearDown(self) -> None:
        pass

    def test_init(self):
        timeline_init = Timeline()
        self.assertEqual(timeline_init.collection, [])

    def test_add_instance(self):
        previous_first_video = self.timeline.collection[0]
        previous_head = self.timeline.head
        previous_video_before = \
            self.timeline.collection[0].previous_instance
        self.assertEqual(previous_video_before, None)
        self.timeline.add_instance(explorer.collection[0], 0)
        new_first_video = self.timeline.collection[0]
        new_head = self.timeline.head
        new_video_before = \
            self.timeline.collection[1].previous_instance
        self.assertEqual(new_video_before, new_first_video)
        self.assertEqual(previous_head, new_head)
        self.assertNotEqual(previous_first_video, new_first_video)
        self.assertEqual(len(self.timeline.collection), 2)
        self.assertNotEqual(self.timeline.collection[0].file,
                         test_video,
                         self.timeline.collection[1].file)
        self.assertEqual(self.timeline.collection[0] == test_video,
                         self.timeline.collection[1] == test_video,
                         self.timeline.collection[0]
                         == self.timeline.collection[1])
        self.assertEqual(self.timeline.collection[0].file.path,
                         self.timeline.collection[1].file.path,
                         test_video.path)

        previous_number_one_element = self.timeline.collection[1]
        self.timeline.add_instance(explorer.collection[0], 1)
        new_number_one_element = self.timeline.collection[1]
        self.assertEqual(len(self.timeline.collection), 3)
        self.assertNotEqual(previous_number_one_element, new_number_one_element)
        self.assertNotEqual(self.timeline.collection[1].file, test_video)
        self.assertEqual(self.timeline.collection[0].file.path,
                         self.timeline.collection[1].file.path,
                         self.timeline.collection[2].file.path)

    def test_remove_instance(self):
        self.timeline.remove_instance(self.timeline.collection[0])
        self.assertEqual(len(self.timeline.collection), 0)
        self.assertEqual(self.timeline.head, None)
        self.timeline.add_instance(explorer.collection[0])
        self.assertEqual(self.timeline.head, self.timeline.collection[0])
        self.timeline.add_instance(explorer.collection[0])
        self.assertEqual(self.timeline.head, self.timeline.collection[1])
        self.assertEqual(len(self.timeline.collection), 2)
        self.assertNotEqual(self.timeline.collection[0].file, test_video)
        self.assertNotEqual(self.timeline.collection[1].file, test_video)
        self.timeline.add_instance(explorer.collection[0], 1)
        self.timeline.remove_instance(self.timeline.collection[1])
        self.assertEqual(len(self.timeline.collection), 2)
        self.timeline.remove_instance(self.timeline.collection[0])
        self.assertEqual(len(self.timeline.collection), 1)
        self.assertNotEqual(self.timeline.collection[0].file, test_video)
        self.assertEqual(self.timeline.head, self.timeline.collection[0])
        self.assertEqual(self.timeline.collection[0].file.path,
                         test_video.path)
        self.timeline.remove_instance(self.timeline.collection[0])
        self.assertEqual(len(self.timeline.collection), 0)
        self.assertEqual(self.timeline.head, None)


class TestTimelineInstance(unittest.TestCase):
    def setUp(self):
        self.timeline = Timeline()
        self.timeline.add_instance(explorer.collection[0])
        self.timeline_instance = self.timeline.collection[0]

    def tearDown(self) -> None:
        pass

    def test_init(self):
        instance = TimelineInstance(explorer.collection[0])
        self.assertNotEqual(instance.file, explorer.collection[0].file)
        self.assertEqual(instance.next_instance, None)
        self.assertEqual(instance.previous_instance, None)
        self.assertEqual(instance.parent, explorer.collection[0])

    def test_change_volume(self):
        self.timeline.add_instance(explorer.collection[0])
        self.timeline.collection[0].change_volume(0.5)
        self.timeline.collection[1].change_volume(2)
        self.assertFalse(
            (self.timeline.collection[0].file.content.audio.to_soundarray()
             == self.timeline.collection[1].file.content.audio.to_soundarray()
             ).all())
        self.timeline.collection[1].change_volume(0.5)
        self.assertTrue(
            (self.timeline.collection[0].file.content.audio.to_soundarray()
             == self.timeline.collection[
                 1].file.content.audio.to_soundarray()).all())

    def test_change_speed(self):
        self.timeline.add_instance(explorer.collection[0])
        self.timeline.collection[0].change_speed(0.5)
        self.timeline.collection[1].change_speed(2)
        self.assertFalse(
            self.timeline.collection[0].file.content.duration
            == self.timeline.collection[1].file.content.duration)
        self.assertEqual(self.timeline.collection[0].file.content.duration,
                         self.timeline.collection[1].file.content.duration * 4)
