import os
import re
from moviepy.editor import VideoFileClip, AudioFileClip


def convert_video_to_audio_moviepy(video_file, new_dir, output_ext="mp3"):
    """Converts video to audio using MoviePy library
    that uses `ffmpeg` under the hood"""
    filename, ext = os.path.splitext(video_file)
    filename = new_dir + "/" + filename.split("/")[-1]
    try:
        clip = VideoFileClip(video_file)
    except KeyError as error:
        print(error)
        clip = AudioFileClip(video_file)
        clip.write_audiofile(f"{filename}.{output_ext}")
    else:
        clip.audio.write_audiofile(f"{filename}.{output_ext}")
    return f"{filename.split('/')[-1]}.{output_ext} "

# def convert(file_list: list):
#     for file in file_list:
#         convert_video_to_audio_moviepy(file )
#     return True


def get_files(folder_path):
    files = os.scandir(folder_path)
    file_list = []
    for file in files:
        name = file.name
        if name.endswith((".mp4", ".mkv", ".avi")):
            file_list.append(file)
    return file_list


def create_save_dir(dir_path, save_folder=None):
    if save_folder is None:
        save_dir = "".join(re.split(r"(/)",dir_path)[:-1]) + "converted_audio"
    else:
        save_dir = save_folder
    try:
        os.mkdir(save_dir)
    except FileExistsError as error:
        pass
    finally:
        return save_dir
