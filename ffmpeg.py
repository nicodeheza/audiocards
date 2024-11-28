from os.path import dirname, join, exists
import requests
import zipfile
import os
import json
import subprocess
from anki.hooks import addHook


class FFmpegInstaller:
    def __init__(self):
        self.addonPath = dirname(__file__)
        self.can_convert = False

        self.ffmpeg_filename = "ffmpeg.exe"
        self.full_ffmpeg_path = join(self.addonPath, self.ffmpeg_filename)

    def GetFFmpegIfNotExist(self):
        if exists(self.full_ffmpeg_path) or self.can_convert:
            self.can_convert = True
            return

        speakers_response = requests.get("https://ffbinaries.com/api/v1/version/6.1")
        download_url = None
        if speakers_response.status_code == 200:
            binaries_json = json.loads(speakers_response.content)
            download_url = binaries_json['bin']['windows-64']['ffmpeg']
        else:
            return
        
        try:
            temp_file_path = join(self.addonPath, "ffmpeg.zip")
            # Download zip
            with requests.get(download_url, stream=True) as ffmpeg_request:
                ffmpeg_request.raise_for_status()
                with open(temp_file_path, 'wb') as ffmpeg_file:
                    total_bytes = int(ffmpeg_request.headers['Content-Length'])
                    bytes_so_far = 0
                    for chunk in ffmpeg_request.iter_content(chunk_size=8192):
                        if chunk:
                            bytes_so_far += len(chunk)
                            ffmpeg_file.write(chunk)
            # Extract zip
            with zipfile.ZipFile(temp_file_path) as zf:
                zf.extractall(dirname(self.full_ffmpeg_path))
            if exists(self.full_ffmpeg_path):
                os.remove(temp_file_path)
                self.can_convert = True
        except:
            print("FFmpeg failed")

ffmpegInstaller = FFmpegInstaller()

def callFfmpegCommand(command: list):
    if not ffmpegInstaller.can_convert:
        return None
    try:
        command = [ffmpegInstaller.full_ffmpeg_path] +  command
        subprocess.run(command, shell=True)

    except Exception as e :
        print("Error running ffmpg command:", e)
        return None

def convertToMp3(file_path:str, new_filename: str):
    #ffmpeg -i input.wav -vn -ar 44100 -ac 2 -b:a 192k output.mp3
    command = ["-i", file_path, "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", new_filename]
    callFfmpegCommand(command)

def concat_audio(front_file:str, back_file:str, silence_duration: int, add_bip: bool, output_file:str, pattern:str):
    #ffmpeg -y -i input1.mp3 -f lavfi -i aevalsrc=0:d=2 -i input2.mp3 -f lavfi -i aevalsrc=0:d=2 -i input3.mp3 -filter_complex "[0][1][2][3][4]concat=n=5:v=0:a=1[outa]" -map "[outa]" output.mp3
    files_count = 0 
    files_i = []
    if add_bip:
        files_count +=1
        files_i.append('-i')
        files_i.append(f'{dirname(__file__)}\\bip.mp3')
    for d in pattern:
        files_count+=2
        if d == "f":
            files_i.append('-i')
            files_i.append(front_file)
        else:
            files_i.append('-i')
            files_i.append(back_file)

        files_i.append("-f")
        files_i.append("lavfi")
        files_i.append("-i")
        files_i.append(f"aevalsrc=0:d={silence_duration}")

    
    a = ""
    for i in range(files_count):
        a+= f"[{i}]"
    a += f"concat=n={files_count}:v=0:a=1[outa]"

    command = ["-y"] + files_i + ["-filter_complex"] + [a] + ["-map"] + ['[outa]'] + [output_file]
    callFfmpegCommand(command)

addHook("profileLoaded", ffmpegInstaller.GetFFmpegIfNotExist)


    
