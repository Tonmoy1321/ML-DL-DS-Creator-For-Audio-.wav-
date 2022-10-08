from __future__ import  unicode_literals
import youtube_dl 
import sys, os, shutil
from pydub import AudioSegment
from pydub.utils import make_chunks
from tqdm import tqdm 


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
} 

yt_url = sys.argv[1] 

folder_path1 = r'C:\Users\ivans\Desktop\499A-UCL-Dataset\Audio Files'
folder_path2 = r'C:\Users\ivans\Desktop\499A-UCL-Dataset\Chunked Audio Files'
folder_path3 = r'C:\Users\ivans\Desktop\499A-UCL-Dataset\Chunked Audio Files\Test'
folder_path4 = r'C:\Users\ivans\Desktop\499A-UCL-Dataset\Chunked Audio Files\Train'

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    print("Downloading Audio from:{}".format(yt_url))
    os.chdir(folder_path1)
    try:
        audiofile = ydl.download([yt_url]) #downloading the audio from youtube video
    except Exception:
        pass


#converting downloaded file to .wav format
file_list = os.listdir() 
for file in file_list:
    input_file = file
    output_file = file + ".wav"
  
# convert mp3 file to wav file
sound = AudioSegment.from_mp3(input_file)
sound.export(output_file, format="wav")  
os.remove(input_file)

#processing downloaded audio into chunks
def process_chunks(audio_file):
    audio = AudioSegment.from_wav(audio_file)
    audio_file_length = len(audio) 
    interval = 4000 #chunk Size in ms 
    overlap = 500 #overlapping 5 ms  
    counter = 0

    end_of_audio = 0 
    for i in range(0, 2 * audio_file_length, interval):
        if i == 0:
            start = 0
            end = interval
        else:
            start = end - overlap
            end = start + interval 
        
        if end >= audio_file_length:
            end = audio_file_length
            end_of_audio = 1 
        
        chunk = audio[start:end] 
        filename = audio_file+str(counter)+'.wav'
        chunk.export(filename, format ="wav")
        # Print information about the current chunk
        print("Processing chunk "+str(counter)+". Start = "
                        +str(start)+" end = "+str(end))
        counter = counter + 1 

        if end_of_audio == 1:
            break 

def make_folder(name):
    os.chdir(folder_path3)
    if os.path.isdir(r"C:\Users\ivans\Desktop\499A-UCL-Dataset\Chunked Audio Files\Test\{}".format(name)) == False:
        os.mkdir(folder_name)
    os.chdir(folder_path4)
    if os.path.isdir(r"C:\Users\ivans\Desktop\499A-UCL-Dataset\Chunked Audio Files\Train\{}".format(name)) == False:
        os.mkdir(folder_name)
    os.chdir(folder_path1)


def move_parent_file():
    os.chdir(folder_path1)
    file_list = os.listdir()
    for p_file in file_list:
        src_p = r'C:\Users\ivans\Desktop\499A-UCL-Dataset\Audio Files\{}'.format(p_file)
        dest_p = r'C:\Users\ivans\Desktop\499A-UCL-Dataset\Downloaded Audio Files' 
        shutil.move(src_p, dest_p)


wav_files = os.listdir() 

for wav_file in wav_files:
    process_chunks(wav_file) 


chunked_files = os.listdir()
file_number = len(chunked_files)
for_training = round((file_number-1)*70/100)
print(for_training)
msg = "Number of Chunk files generated: {}".format(file_number-1)
print(msg) 
print ("Moving Chunked files to specific folder:->") 
folder_name = sys.argv[2].upper() 

make_folder(folder_name)

for chunk_file in chunked_files[1:for_training]:
    source = r"C:\Users\ivans\Desktop\499A-UCL-Dataset\Audio Files\{}".format(chunk_file)
    dest = r"C:\Users\ivans\Desktop\499A-UCL-Dataset\Chunked Audio Files\Test\{}".format(folder_name)
    shutil.move(source, dest) 


test_files = os.listdir()
for chunk_file in test_files[1:]:
    source = r"C:\Users\ivans\Desktop\499A-UCL-Dataset\Audio Files\{}".format(chunk_file)
    dest = r"C:\Users\ivans\Desktop\499A-UCL-Dataset\Chunked Audio Files\Train\{}".format(folder_name)
    shutil.move(source, dest) 


move_parent_file()
print("Done!")

     


    




