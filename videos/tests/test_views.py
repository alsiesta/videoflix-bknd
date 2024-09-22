from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from videos.models import Video, Category
from django.core.files.uploadedfile import SimpleUploadedFile

class VideoViewTest(TestCase):

    def setUp(self):
        # Create a user and a token
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.is_active = True  # Ensure the user is active
        self.user.save()  # Save the user to apply the changes
        self.token = Token.objects.create(user=self.user)
        
        # Create a category
        self.category = Category.objects.create(name="Test Category")
        
        # Create a video
        self.video_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")
        self.image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.video = Video.objects.create(
            title="Test Video",
            description="Test Description",
            video_file=self.video_file,
            image_file=self.image_file,
            path="test_video.mp4",
            imagepath="test_image.jpg"
        )
        self.video.categories.add(self.category)
        
        # Initialize the API client
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_all_videos_view(self):
        response = self.client.get(reverse('all_videos'))
        self.assertEqual(response.status_code, 200)
        
        # Verify the response content
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['title'], self.video.title)
        self.assertEqual(response_data[0]['description'], self.video.description)
        self.assertEqual(response_data[0]['path'], self.video.path)
        self.assertEqual(response_data[0]['imagepath'], self.video.imagepath)
        self.assertEqual(response_data[0]['categories'][0]['name'], self.category.name)

    def test_video_detail_view(self):
        response = self.client.get(reverse('get_video_by_id', args=[self.video.id]))
        self.assertEqual(response.status_code, 200)
        
        # Print the response data for debugging
        response_data = response.json()
        print(response_data)
        
        # Verify the response content
        self.assertEqual(response_data['title'], self.video.title)
        self.assertEqual(response_data['description'], self.video.description)
        self.assertEqual(response_data['path'], self.video.path)
        self.assertEqual(response_data['imagepath'], self.video.imagepath)
        self.assertIn(self.category.id, response_data['categories'])