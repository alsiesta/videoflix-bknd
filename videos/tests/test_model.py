from django.test import TestCase
from videos.models import Video, Category
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class VideoModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.video_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")
        self.image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.video = Video.objects.create(
            title="Test Video",
            description="Test Description",
            video_file=self.video_file,
            image_file=self.image_file
        )
        self.video.categories.add(self.category)

    def test_video_creation(self):
        self.assertEqual(self.video.title, "Test Video")
        self.assertEqual(self.video.description, "Test Description")
        self.assertTrue(self.video.video_file.name.endswith(".mp4"))
        self.assertTrue(self.video.image_file.name.endswith(".jpg"))
        self.assertIn(self.category, self.video.categories.all())

    def test_video_path(self):
        self.video.save()
        self.assertTrue(self.video.path.endswith(".m3u8"))

    def test_image_path(self):
        self.video.save()
        self.assertTrue(self.video.imagepath.endswith(".jpg"))

    def tearDown(self):
        if os.path.exists(self.video.video_file.path):
            os.remove(self.video.video_file.path)
        if os.path.exists(self.video.image_file.path):
            os.remove(self.video.image_file.path)