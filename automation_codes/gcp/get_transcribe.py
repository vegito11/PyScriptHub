import io
import os
import requests
# from google.cloud import speech
import ffmpeg
import requests
import openai
from moviepy.editor import *
import whisper

global audioFolder
audioFolder = "audio"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "key.json"

def get_video_content(path, url=False):

    video_content = None
    if url:
        # Download video file from URL
        response = requests.get(path)
        video_content = response.content

    else:
        # Read video file
        with io.open(path, "rb") as video_file:
            video_content = video_file.read()

    return video_content

def create_audio_file(video_path, audio_op_path):
    
  stream = ffmpeg.input(video_path)
  stream = ffmpeg.output(stream, audio_op_path)
  ffmpeg.run(stream)

  print(f"Extracted audio from video and saved at {audio_op_path} ")



def transcribe(audio_path, lang="en"):
    
    result_file = f"output_transcript/{audio_path.split('/')[1]}.txt"
    result = model.transcribe(audio_path, language=lang)
    
    print(f"Extracted Text from audio and saved at {result_file} ")

    with open(result_file, "w", encoding="utf-8") as f:
        # print(result["text"])
        f.write(result["text"])

model = whisper.load_model("base")

def worker():

    for vid in range(30, 31):
        
        video_filepath = f"input_video/Day_{vid}.mp4"
        audio_op_path = f"audio/Day_{vid}.mp3"
        
        result_file = f"output_transcript/{audio_op_path.split('.mp3')[0]}.txt"
        print(f" ------ {vid}) Processing Video {video_filepath} ----- ")

        print(result_file)
        # create_audio_file(video_filepath, audio_op_path)
        transcribe(audio_op_path, lang="en" )

        print("-------========="*10)


if __name__ == '__main__':
    worker()


'''
!pip install -q openai
!pip install -q pytube
!pip install -q ffmpeg-python
!pip install -q git+https://github.com/openai/whisper.git
https://www.videohelp.com/software/ffmpeg
python -m pip install --upgrade googletrans==4.0.0-rc1 
'''
