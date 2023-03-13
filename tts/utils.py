import datetime
from pathlib import Path
from django.conf import settings
import PyPDF2
import pyttsx3
import wave
from uuid import uuid4
from tts.models import podcast_files
import sys
import os
import datetime
import hashlib
import hmac
import urllib.request
import requests
from moviepy.editor import concatenate_audioclips, AudioFileClip

BASE_DIR = Path(__file__).resolve().parent.parent

def extract_text(filename):
    pdfFileObj = open(filename, "rb")
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    count = 0
    mytext = ""
    for pageNum in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)
        mytext += pageObj.extractText()
        count += len(mytext.split("\n"))
    pdfFileObj.close()
    return mytext, count


def convert_pdf_to_audio(instance):
    text, count = extract_text(instance.pdf.path)
    import os
    filepath = os.path.join(settings.BASE_DIR, f'media/recs/{uuid4()}.wav')
    store_audio_file(filepath, text)
    return filepath, text, count


def convert_text_to_audio(speaker, script, name):
    
 
    aws_generate_clips_taskId(speaker, script, name)


def save_excel(name):
    # text = extract_text(instance.pdf.path)
    import os
    # name.split("_").join(" ")
    filepath = os.path.join(settings.BASE_DIR, f'media/excel/{name}')
    return filepath
    


def store_audio_file(speaker, filepath, script, filename):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    # voices = engine.getProperty("voices")
    import os

    clips = []
    speaker2 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    speaker1 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enIN_RaviM"

    for x in range(len(script)):
        spkr = speaker[x]
        if (spkr == "speaker1"):
            engine.setProperty('voice', speaker1)
            filepath = os.path.join(settings.BASE_DIR, f'media/clips/{x}.wav')
            clips.append(filepath)
            engine.save_to_file(script[x], filepath)
            engine.runAndWait()
            engine.stop()
        else:
            engine.setProperty('voice', speaker2)
            filepath = os.path.join(settings.BASE_DIR, f'media/clips/{x}.wav')
            clips.append(filepath)
            engine.save_to_file(script[x], filepath)
            engine.runAndWait()
            engine.stop()

    merge_audio_file(clips, filename)


def merge_mp3(audio_clip_paths, name):
    import os
    # output_path = os.path.join(BASE_DIR, f'media/podcast/{name}.mp3')
    output_path = f'podcast/{name}.mp3'
    clips = [AudioFileClip(c) for c in audio_clip_paths]
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_path)
    podcast = podcast_files(
        file_name=name, date_time=datetime.date, audio_file=output_path)
    podcast.save()
    for clip in audio_clip_paths:
        os.remove(clip)
    

    
def merge_audio_file(audio_clip_paths, name):
    data = []
    for clip in audio_clip_paths:
        w = wave.open(clip, "rb")
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()
    import os
    output_path = os.path.join(BASE_DIR, f'media/podcast/{name}.wav')
    output = wave.open(output_path, "wb")
    output.setparams(data[0][0])
    for i in range(len(data)):
        output.writeframes(data[i][1])
    output.close()
    podcast = podcast_files(
        file_name=name, date_time=datetime.date, audio_file=output_path)
    podcast.save()
    # for clip in audio_clip_paths:
    #     os.remove(clip)
    pt=os.path.join(BASE_DIR, 'media/',"clips//")
    for files_name in os.listdir(pt):
        file =pt+files_name
        if os.path.exists(file):
            print("Deleting file")
            os.remove(file)
    


def aws_generate_clips_taskId(speaker, script, filename):
    clips_url = []
    for x in range(len(script)):
        access_key = 'AKIA6N53FKRFDPJHRRTN'
        secret_key = '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'
        if access_key is None or secret_key is None:
            print('No access key is available.')
            sys.exit()

        method = 'POST'
        service = 'polly'
        region = 'us-east-1'
        host = service+'.'+region+'.amazonaws.com'
        api = '/v1/synthesisTasks'
        endpoint = 'https://'+host+api
        content_type = 'application/json'
        script1 ="<speak>"
        script1 += script[x]
        script1 += "</speak>"
        newstring = script1.replace(".","<break time='1s'/>").replace("?","<break time='1s'/>")
        # newstring =  script1.replace("?","<break time='1s'/>")
        # newstring =  script1.replace('"',"&quot;")
        # newstring =  script1.replace("&","&amp;")
        # newstring =  script1.replace("'","&apos;")
        # newstring =  script1.replace("<","&lt;")
        # newstring =  script1.replace(">","&gt;")


        print(newstring)
        speaker1 = speaker[x]
        request_parameters = '{'
        request_parameters += '"Engine": "neural",'
        request_parameters += '"OutputFormat": "mp3",'
        # request_parameters +=  '"OutputFormat": "en-US",'
        request_parameters += '"TextType": "ssml",'
        request_parameters += '"SampleRate": "8000",'
        # request_parameters +=  '"SpeechMarkTypes": "ssml",'
        request_parameters += '"OutputS3BucketName": "myvoicebucket123",'
        request_parameters += '"Text"'+':' + '"%s" ,' % newstring
        request_parameters += '"VoiceId" '+':' '"%s"' % speaker1
        request_parameters += '}'

        def sign(key, msg):
            return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

        def getSignatureKey(key, dateStamp, regionName, serviceName):
            kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
            kRegion = sign(kDate, regionName)
            kService = sign(kRegion, serviceName)
            kSigning = sign(kService, 'aws4_request')
            return kSigning

        # Create a date for headers and the credential string
        t = datetime.datetime.utcnow()
        # Format date as YYYYMMDD'T'HHMMSS'Z'
        amz_date = t.strftime('%Y%m%dT%H%M%SZ')
        # Date w/o time, used in credential scope
        datestamp = t.strftime('%Y%m%d')

        canonical_uri = api  # '/'
        canonical_querystring = ''

        canonical_headers = 'content-type:' + content_type + '\n' + \
            'host:' + host + '\n' + 'x-amz-date:' + amz_date + '\n'

        # signed_headers = 'host'
        signed_headers = 'content-type;host;x-amz-date'

        payload_hash = hashlib.sha256(
            request_parameters.encode('utf-8')).hexdigest()

        canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + \
            '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = datestamp + '/' + region + \
            '/' + service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' + amz_date + '\n' + credential_scope + \
            '\n' + \
            hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

        signing_key = getSignatureKey(secret_key, datestamp, region, service)

        signature = hmac.new(signing_key, (string_to_sign).encode(
            "utf-8"), hashlib.sha256).hexdigest()

        authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + \
            credential_scope + ', ' + 'SignedHeaders=' + \
            signed_headers + ', ' + 'Signature=' + signature

        headers = {'Content-Type': content_type,
                   'X-Amz-Date': amz_date,
                   # 'X-Amz-Target':amz_target, # not used by polly
                   'Authorization': authorization_header}

        print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
        # print ('Request URL = ' + endpoint)

        response = requests.post(
            endpoint, data=request_parameters, headers=headers)
        print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
        print('Response code: %d\n' % response.status_code)

        url = response.json()['SynthesisTask']['TaskId']
        # print(url)
        clips_url.append(url)
    print(clips_url)
    import time
    time.sleep(15)
    download(clips_url, filename)
#  aws_generate_clips_download(clips_url,filename)

    # import time
    # time.sleep(15)
    # filepath = os.path.join(settings.BASE_DIR, f'media/clips/{x}.mp3')
    # urllib.request.urlretrieve(url, filepath)
    # clips.append(filepath)

#  merge_mp3(clips,filename)


def aws_generate_clips_download(clips_url, filename):
    clips = []
    for x in clips_url:
        access_key = 'AKIA6N53FKRFDPJHRRTN'
        secret_key = '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'
        if access_key is None or secret_key is None:
            print('No access key is available.')
            sys.exit()

        method = 'POST'
        service = 'polly'
        region = 'us-east-1'
        host = service+'.'+region+'.amazonaws.com'
        api = '/v1/synthesisTasks'
        endpoint = 'https://'+host+api
        content_type = 'application/json'
        taskId = x
        print(taskId)
        # script1 = script[x]
        # speaker1 = speaker[x]
        # request_parameters = '{'
        # request_parameters +=  '"Engine": "standard",'
        # request_parameters +=  '"OutputFormat": "mp3",'
        # request_parameters +=  '"OutputS3BucketName": "myvoicebucket123",'
        # request_parameters +=  '"Text"'+':'+ '"%s" ,' % script1
        # request_parameters +=  '"VoiceId" '+':' '"%s"' % speaker1
        # request_parameters +=  '}'

        request_parameters = '{'
        request_parameters += '"TaskId" '+':' '"%s"' % taskId
        request_parameters += '}'

        def sign(key, msg):
            return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

        def getSignatureKey(key, dateStamp, regionName, serviceName):
            kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
            kRegion = sign(kDate, regionName)
            kService = sign(kRegion, serviceName)
            kSigning = sign(kService, 'aws4_request')
            return kSigning

        # Create a date for headers and the credential string
        t = datetime.datetime.utcnow()
        # Format date as YYYYMMDD'T'HHMMSS'Z'
        amz_date = t.strftime('%Y%m%dT%H%M%SZ')
        # Date w/o time, used in credential scope
        datestamp = t.strftime('%Y%m%d')

        canonical_uri = api  # '/'
        canonical_querystring = ''

        canonical_headers = 'content-type:' + content_type + '\n' + \
            'host:' + host + '\n' + 'x-amz-date:' + amz_date + '\n'

        # signed_headers = 'host'
        signed_headers = 'content-type;host;x-amz-date'

        payload_hash = hashlib.sha256(
            request_parameters.encode('utf-8')).hexdigest()

        canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + \
            '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = datestamp + '/' + region + \
            '/' + service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' + amz_date + '\n' + credential_scope + \
            '\n' + \
            hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

        signing_key = getSignatureKey(secret_key, datestamp, region, service)

        signature = hmac.new(signing_key, (string_to_sign).encode(
            "utf-8"), hashlib.sha256).hexdigest()

        authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + \
            credential_scope + ', ' + 'SignedHeaders=' + \
            signed_headers + ', ' + 'Signature=' + signature

        headers = {'Content-Type': content_type,
                   'X-Amz-Date': amz_date,
                   # 'X-Amz-Target':amz_target, # not used by polly
                   'Authorization': authorization_header}

        print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
        # print ('Request URL = ' + endpoint)

        response = requests.post(
            endpoint, data=request_parameters, headers=headers)
        print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
        print('Response code: %d\n' % response.status_code)

        url = response.json()['SynthesisTask']['OutputUri']
        # clips_url.append(url)
        # import time
        # time.sleep(15)
        filepath = os.path.join(settings.BASE_DIR, f'media/clips/{x}.mp3')
        urllib.request.urlretrieve(url, filepath)
        clips.append(filepath)

    merge_mp3(clips, filename)


def download(clips_url, filename):
    clips = []
    for x in clips_url:
        ext = '.mp3'
        url = 'https://myvoicebucket123.s3.amazonaws.com/'+x+ext
        # print(url)
        filepath = os.path.join(BASE_DIR, f'media/clips/{x}.mp3')
        urllib.request.urlretrieve(url, filepath)
        print("downloading clip")
        clips.append(filepath)

    merge_mp3(clips, filename)
