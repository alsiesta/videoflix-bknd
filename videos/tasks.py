import subprocess
import os

def convert_to_480p(source):
    base, ext = os.path.splitext(source)
    new_file_name = f"{base}_480p{ext}"
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    print(cmd)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Conversion successful:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error during conversion:", e.stderr)

def convert_to_720p(source):
    base, ext = os.path.splitext(source)
    new_file_name = f"{base}_720p{ext}"
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    print(cmd)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Conversion successful:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error during conversion:", e.stderr)
