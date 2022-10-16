import unittest
import sys
import os
from modules.editor import Video as video

path = os.getcwd()


class TestEditor(unittest.TestCase):
    def setUp(self):
        os.chdir(path.replace('\\', '/').split("/tests")[0])
        tests_dir = os.getcwd() + '/tests'
        sources_dir = tests_dir + '/sources/'
        self.test_video = video(sources_dir + 'video.mp4')

    def tearDown(self) -> None:
        os.chdir(path)

    def test_export(self):
        name = 'test_done'
        self.test_video.export(name)
        export_path = os.getcwd() + '/export/'
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
