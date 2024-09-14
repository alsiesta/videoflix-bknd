import subprocess
import os
import shlex

def convert_video(source, resolution, suffix):
    print('############### Start Video Conversion ###############')
    # file_name, ext = os.path.splitext(source) # Ignore the original extension
    file_name, _ = os.path.splitext(source)
    target = f"{file_name}_{suffix}.m3u8" # Use .m3u8 extension for the playlist
    # target = f"{file_name}_{suffix}.mp4" # Use .m3u8 extension for the playlist
    
    # Convert Windows paths to WSL-compatible Linux paths
    linux_source = "/mnt/" + source.replace("\\", "/").replace('C:', 'c')
    linux_target = "/mnt/" + target.replace("\\", "/").replace('C:', 'c')
    
    # FFmpeg command for Video Transcoding with x264 Codec
    # cmd = f'ffmpeg -i "{linux_source}" -s {resolution} -c:v libx264 -crf 23 -c:a aac -strict -2 "{linux_target}"'
    
    # # FFmpeg command for HLS conversion
    cmd = f'ffmpeg -i "{linux_source}" -s {resolution} -c:v libx264 -crf 23 -c:a aac -strict -2 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{linux_target}"'

    
    try:
        # Use shlex.split to split the command string into a list
        result = subprocess.run(shlex.split(cmd), capture_output=True, text=True, check=True)
        print("Conversion successful:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error during conversion:", e.stderr)
        print("Return code:", e.returncode)
        print("Command output:", e.output)

def convert_to_480p(source):
    convert_video(source, 'hd480', '480p')

def convert_to_720p(source):
    convert_video(source, 'hd720', '720p')
    
def convert_to_1080p(source):
    convert_video(source, 'hd1080', '1080p')