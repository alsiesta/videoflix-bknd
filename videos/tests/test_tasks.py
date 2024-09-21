from django.test import TestCase
from videos.tasks import convert_video
import os
import subprocess
import shutil

class ConvertVideoTest(TestCase):

    def setUp(self):
        self.source_filename = "fitness.mp4"
        self.resolution = "hd720"
        self.suffix = "720p"

        # Determine the correct directory based on the OS
        if os.name == 'nt':  # For Windows
            self.mnt_dir = os.path.join('C:\\', 'mnt')
        else:  # For Unix/Linux/Mac
            self.mnt_dir = '/mnt'

        # Ensure the directory exists
        os.makedirs(self.mnt_dir, exist_ok=True)

        # Paths for the source and target files
        self.source_path = os.path.join(self.mnt_dir, self.source_filename)
        self.target_filename = f"{os.path.splitext(self.source_filename)[0]}_{self.suffix}.m3u8"
        self.target_path = os.path.join(self.mnt_dir, self.target_filename)
        
        # Copy the test video file to the expected location
        test_video_src = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), '..', '..', 'datafortesting', self.source_filename
            )
        )
        if not os.path.exists(test_video_src):
            self.fail(f"Test video file not found: {test_video_src}")
        else:
            # Ensure the destination directory exists
            os.makedirs(os.path.dirname(self.source_path), exist_ok=True)
            shutil.copy(test_video_src, self.source_path)
            
        print(f"Source path: {self.source_path}")
        print(f"Target path: {self.target_path}")
        print(f"Test video source path: {test_video_src}")

    def test_convert_video(self):
        try:
            # Pass only the filename if that's what convert_video expects
            convert_video(self.source_filename, self.resolution, self.suffix)
            # Check if the output file exists at the expected location
            self.assertTrue(os.path.exists(self.target_path), f"Output file not found: {self.target_path}")
        except subprocess.CalledProcessError as e:
            self.fail(f"Conversion failed: {e.stderr}")
        except Exception as e:
            self.fail(f"An unexpected error occurred: {e}")

    def tearDown(self):
        # Remove the source video file
        if os.path.exists(self.source_path):
            os.remove(self.source_path)

        # Remove the generated target file
        if os.path.exists(self.target_path):
            os.remove(self.target_path)
