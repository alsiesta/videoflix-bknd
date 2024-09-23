import subprocess
import os
import shlex
import platform
import logging

from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)

# Detect if the code is running inside WSL.
def is_wsl():
    return 'microsoft' in platform.uname().release.lower()


# Convert a Windows path to a WSL-compatible Linux path.
# Example: C:\Users\User\file.mp4 -> /mnt/c/Users/User/file.mp4
def convert_windows_to_wsl_path(windows_path):
    
    # Remove 'file:' prefix if present
    if windows_path.startswith('file:'):
        windows_path = windows_path[5:]
    
    # Replace backslashes with forward slashes
    windows_path = windows_path.replace('\\', '/')
    
    # Extract drive letter and the rest of the path
    if ':' in windows_path:
        drive, path = windows_path.split(':', 1)
        drive = drive.lower()  # Lowercase the drive letter
        path = path.lstrip('/')  # Remove leading slash if present
        # Construct WSL path
        wsl_path = f"/mnt/{drive}/{path}"
    else:
        # If no drive letter is present, return the path as-is
        wsl_path = windows_path
    
    return wsl_path


# Convert Windows paths to WSL-compatible paths if running in WSL or Windows.
# Otherwise, return the paths as-is.
def get_converted_path(source, target):
    system = platform.system()
    wsl = is_wsl()
    
    if wsl or system == 'Windows':
        # Convert paths to WSL format
        linux_source = convert_windows_to_wsl_path(source)
        linux_target = convert_windows_to_wsl_path(target)
    else:
        # On native Linux systems, use the paths as-is
        linux_source = source
        linux_target = target
    
    print("System:", system)
    print("Is WSL:", wsl)
    print("source: ", linux_source)
    print("target: ", linux_target)
    
    return linux_source, linux_target


# Mapping of suffixes to actual resolution dimensions
RESOLUTION_MAP = {
    '480p': '854x480',
    '720p': '1280x720',
    '1080p': '1920x1080'
}


def convert_video(source, suffix):
    logging.info('############### Start Video Conversion ###############')
    
    # Strip 'file:' prefix if present
    if source.startswith('file:'):
        source = source[5:]
    
    logging.info(f"Original Source Path: {source}")
    
    # Determine the resolution based on suffix
    resolution = RESOLUTION_MAP.get(suffix)
    if not resolution:
        logging.error(f"Invalid suffix '{suffix}'. Available options: {list(RESOLUTION_MAP.keys())}")
        return
    
    source_path = Path(source)
    
    # Construct target path
    target_path = source_path.with_name(f"{source_path.stem}_{suffix}.m3u8")
    
    # Convert paths based on environment
    linux_source, linux_target = get_converted_path(str(source_path), str(target_path))
    
    logging.info(f"Converted Source Path: {linux_source}")
    logging.info(f"Converted Target Path: {linux_target}")
    
    # Check if the source file exists
    if not Path(linux_source).exists():
        logging.error(f"Source file does not exist: {linux_source}")
        return
    
    # FFmpeg command for HLS conversion
    cmd = (
        f'ffmpeg -i "{linux_source}" -s {resolution} '
        f'-c:v libx264 -crf 23 -c:a aac -strict -2 '
        f'-start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{linux_target}"'
    )
    
    logging.info(f"Executing command: {cmd}")
    
    try:
        # Use shlex.split to split the command string into a list
        result = subprocess.run(shlex.split(cmd), capture_output=True, text=True, check=True)
        logging.info("Conversion successful.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during conversion: {e.stderr}")
        logging.error(f"Return code: {e.returncode}")
        logging.error(f"Command output: {e.output}")
        

def convert_to_480p(source):
    convert_video(source, '480p')

def convert_to_720p(source):
    convert_video(source, '720p')

def convert_to_1080p(source):
    convert_video(source, '1080p')
    

# def convert_video(source, resolution, suffix):
#     print('############### Start Video Conversion ###############')
#     # file_name, ext = os.path.splitext(source) # Ignore the original extension
#     file_name, _ = os.path.splitext(source)
#     target = f"{file_name}_{suffix}.m3u8" # Use .m3u8 extension for the playlist
#     # target = f"{file_name}_{suffix}.mp4" # Use .m3u8 extension for the playlist
#     get_converted_path(source, target)
    
#     # Convert Windows paths to WSL-compatible Linux paths
#     linux_source = "/mnt/" + source.replace("\\", "/").replace('C:', 'c')
#     linux_target = "/mnt/" + target.replace("\\", "/").replace('C:', 'c')
    
#     # FFmpeg command for Video Transcoding with x264 Codec
#     # cmd = f'ffmpeg -i "{linux_source}" -s {resolution} -c:v libx264 -crf 23 -c:a aac -strict -2 "{linux_target}"'
    
#     # # FFmpeg command for HLS conversion
#     cmd = f'ffmpeg -i "{linux_source}" -s {resolution} -c:v libx264 -crf 23 -c:a aac -strict -2 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{linux_target}"'


#     print("My code source: ", linux_source)
#     print("My code target: ", linux_target)
    
#     try:
#         # Use shlex.split to split the command string into a list
#         result = subprocess.run(shlex.split(cmd), capture_output=True, text=True, check=True)
#         print("Conversion successful:", result.stdout)
#     except subprocess.CalledProcessError as e:
#         print("Error during conversion:", e.stderr)
#         print("Return code:", e.returncode)
#         print("Command output:", e.output)

# def convert_to_480p(source):
#     convert_video(source, 'hd480', '480p')

# def convert_to_720p(source):
#     convert_video(source, 'hd720', '720p')
    
# def convert_to_1080p(source):
#     convert_video(source, 'hd1080', '1080p')