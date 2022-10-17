import unittest
import os
from modules.timeline import Timeline
from modules.explorer import Explorer
from modules.editor import Video as video

path = os.getcwd()
os.chdir(path.replace('\\', '/').split("/tests")[0])
tests_dir = os.getcwd() + '/tests'
sources_dir = tests_dir + '/sources/'
os.chdir(path)
test_video = video(sources_dir + 'video.mp4')
explorer = Explorer()
explorer.add_item(test_video)


class TestTimeline(unittest.TestCase):
    def setUp(self):
        self.timeline = Timeline()

    def tearDown(self) -> None:
        pass

    def test_init(self):
        self.assertEqual(self.timeline.collection, [])

    def test_add_instance(self):
        self.timeline.add_instance(explorer, test_video)
        self.assertEqual(len(self.timeline.collection), 1)
        self.assertNotEqual(self.timeline.collection[0].video, test_video)
        self.assertTrue(
            self.timeline.collection[0].video.video == test_video.video)
        self.assertEqual(self.timeline.head, self.timeline.collection[0])

        previous_first_video = self.timeline.collection[0]
        previous_head = self.timeline.head
        previous_video_before = \
            self.timeline.collection[0].previous_video_instance
        self.assertEqual(previous_video_before, None)
        self.timeline.add_instance(explorer, test_video, 0)
        new_first_video = self.timeline.collection[0]
        new_head = self.timeline.head
        new_video_before = \
            self.timeline.collection[1].previous_video_instance
        self.assertEqual(new_video_before, new_first_video)
        self.assertEqual(previous_head, new_head)
        self.assertNotEqual(previous_first_video, new_first_video)
        self.assertEqual(len(self.timeline.collection), 2)
        self.assertTrue(
            self.timeline.collection[0].video.video == test_video.video,
            self.timeline.collection[1].video.video == test_video.video)
        self.assertFalse(self.timeline.collection[0].video == test_video,
                         self.timeline.collection[1].video == test_video)
