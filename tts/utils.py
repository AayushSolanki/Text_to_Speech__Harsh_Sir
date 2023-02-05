import datetime
from django.conf import settings
import PyPDF2
import pyttsx3
import wave
from uuid import uuid4

from tts.models import podcast_files

def extract_text(filename):
    pdfFileObj = open(filename, "rb")
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    count=0
    mytext = ""
    for pageNum in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)
        mytext += pageObj.extractText()
        count+= len(mytext.split("\n"))
    pdfFileObj.close()
    return mytext,count


def convert_pdf_to_audio(instance):
    text,count = extract_text(instance.pdf.path)
    import os
    filepath = os.path.join(settings.BASE_DIR, f'media/recs/{uuid4()}.wav')
    store_audio_file(filepath, text)
    return filepath, text , count

def convert_text_to_audio(speaker,script,name):
  
    # text = extract_text(instance.pdf.path)
    import os
    filepath = os.path.join(settings.BASE_DIR, f'media/recs/{name}.wav')
    store_audio_file(speaker,filepath, script,name)

def save_excel(name):
  
    # text = extract_text(instance.pdf.path)
    import os
    filepath = os.path.join(settings.BASE_DIR, f'media/excel/{name}')
    return filepath


def store_audio_file(speaker,filepath, script,filename):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    # voices = engine.getProperty("voices")
    import os
   
    clips=[]
    speaker2="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    speaker1="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enIN_RaviM"
    for x in range(len(script)):
        spkr = speaker[x]
        if(spkr=="speaker1"):
         engine.setProperty('voice',speaker1)
         filepath = os.path.join(settings.BASE_DIR, f'media/clips/{x}.wav')
         clips.append(filepath)
         engine.save_to_file(script[x], filepath)
         engine.runAndWait()
         engine.stop()
        else:
         engine.setProperty('voice',speaker2)
         filepath = os.path.join(settings.BASE_DIR, f'media/clips/{x}.wav')
         clips.append(filepath)
         engine.save_to_file(script[x], filepath)
         engine.runAndWait()
         engine.stop()  
         
    merge_audio_file(clips,filename)

def merge_audio_file(audio_clip_paths,name):
    data = []
    for clip in audio_clip_paths:
        w = wave.open(clip, "rb")
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()
    import os
    output_path = os.path.join(settings.BASE_DIR, f'media/podcast/{name}.wav')
    output = wave.open(output_path, "wb")
    output.setparams(data[0][0])
    for i in range(len(data)):
        output.writeframes(data[i][1])
    output.close()
    podcast = podcast_files(file_name=name,date_time =datetime.date,audio_file=output_path)
    podcast.save()
    for clip in audio_clip_paths:

     os.remove(clip)


