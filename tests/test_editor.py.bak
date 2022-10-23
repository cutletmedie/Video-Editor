import unittest
import sys
import os
from modules.editor import Video as video
from modules.editor import VideoFragment as video_fragment
from modules.changes_history import Actions
import copy

path = os.getcwd()
prev_tests_dir = path.replace('\\', '/').split("/tests")[0]
export_path = prev_tests_dir + '/export/'
tests_dir = prev_tests_dir + '/tests'
sources_dir = tests_dir + '/sources/'
test_video = video(sources_dir + 'video.mp4')


class TestVideo(unittest.TestCase):
    def setUp(self):
        self.test_video = video(sources_dir + 'video.mp4')

    def tearDown(self) -> None:
        pass

    def test_export(self):
        name = 'test_done'
        self.test_video.export(name)
        self.assertTrue(os.path.isfile(export_path + name + '.mp4'))
        os.remove(export_path + name + '.mp4')

    def test_volume(self):
        previous_volume = self.test_video.video.audio.to_soundarray()
        self.test_video.volume(0.5)
        new_volume = self.test_video.video.audio.to_soundarray()
        self.assertFalse((previous_volume == new_volume).all())

    def test_speed(self):
        previous_duration = self.test_video.video.duration
        self.test_video.video_speed(2)
        new_duration = self.test_video.video.duration
        self.assertEqual(previous_duration / 2, new_duration)

        self.test_video.video_speed(0.5)
        new_duration = self.test_video.video.duration
        self.assertEqual(previous_duration, new_duration)

    def test_crop(self):
        previous_duration = self.test_video.video.duration
        expected_frame = self.test_video.video.get_frame(10)
        self.test_video.crop(10, 30)
        new_duration = self.test_video.video.duration
        new_first_frame = self.test_video.video.get_frame(0)
        self.assertNotEqual(previous_duration, new_duration)
        self.assertTrue((expected_frame == new_first_frame).all())


class TestVideoFragment(unittest.TestCase):
    def setUp(self):
        self.empty_fragment = video_fragment()
        self.test_video = video(sources_dir + 'video.mp4')

    def tearDown(self) -> None:
        pass

    def test_init(self):
        fragment = video_fragment(self.test_video)
        self.assertEqual(len(fragment.content), 1)

    def test_add_video(self):
        self.empty_fragment.add_video(self.test_video)
        self.assertEqual(len(self.empty_fragment.content), 1)
        self.assertEqual(
            self.test_video.video.duration, self.empty_fragment.duration)

    def test_remove_video(self):
        self.empty_fragment.add_video(self.test_video)
        self.empty_fragment.remove_video(self.empty_fragment.content[0])
        self.assertEqual(len(self.empty_fragment.content), 0)

    def test_change_fragment_volume(self):
        self.empty_fragment.add_video(self.test_video)
        previous_volume = \
            self.empty_fragment.content[0].video.audio.to_soundarray()
        self.empty_fragment.change_fragment(Actions.VOLUME, n=0.5)
        new_volume = self.empty_fragment.content[0].video.audio.to_soundarray()
        self.assertFalse((previous_volume == new_volume).all())

    def test_change_fragment_speed(self):
        self.empty_fragment.add_video(self.test_video)
        previous_duration = self.empty_fragment.duration
        self.empty_fragment.change_fragment(Actions.SPEED, n=2)
        new_duration = self.empty_fragment.duration
        self.assertEqual(previous_duration / 2, new_duration)

        self.empty_fragment.change_fragment(Actions.SPEED, n=0.25)
        new_duration = self.empty_fragment.duration
        self.assertEqual(previous_duration * 2, new_duration)

    def test_change_fragment_crop(self):
        self.empty_fragment.add_video(self.test_video)
        self.test_video.crop(5, 20)
        self.empty_fragment.add_video(self.test_video)
        previous_duration = self.empty_fragment.duration
        expected_frame1 = self.empty_fragment.content[0].video.get_frame(10)
        expected_frame2 = self.empty_fragment.content[1].video.get_frame(0)
        self.empty_fragment.change_fragment(Actions.CROP, start=10, end=30)
        new_duration = self.empty_fragment.duration
        new_first_frame1 = self.empty_fragment.content[0].video.get_frame(0)
        new_first_frame2 = self.empty_fragment.content[1].video.get_frame(0)
        self.assertNotEqual(previous_duration, new_duration)
        self.assertTrue((expected_frame1 == new_first_frame1).all())
        self.assertTrue((expected_frame2 == new_first_frame2).all())

    def test_change_fragment_export(self):
        self.empty_fragment.add_video(self.test_video)
        self.empty_fragment.change_fragment(
            Actions.EXPORT, name='test_fragment', path=export_path)
        self.assertTrue(os.path.isfile(export_path + 'test_fragment.mp4'))
        os.remove(export_path + 'test_fragment.mp4')
