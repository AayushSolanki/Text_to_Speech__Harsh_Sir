import datetime
from django.shortcuts import render
from tts.models import audio, podcast_files,excel_files
from .utils import  convert_text_to_audio, merge_audio_file
import PyPDF2
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def mergeaudio(request):
 clips = audio.objects.all()
 
 return render(request,"merge.html",{'clips':clips})

def merge_dailogs(request):
   if request.method == "POST":
     script = request.POST.getlist('selected_audio[]')
     speaker = request.POST.getlist('selected_speaker[]')
     filename = request.POST.get('filename')

     convert_text_to_audio(speaker,script,filename)

     podcasts = podcast_files.objects.all()
     return render(request,"display_result.html",{'podcasts':podcasts})
    
   else:
      podcasts = podcast_files.objects.all()
      return render(request,"display_result.html",{'podcasts':podcasts})

def merge_files(request):
   if request.method == "POST":
     name = request.POST.get('filename')
     clip = request.POST.getlist('selected_audio[]')

     merge_audio_file(clip,name)
   #   podcast = podcast_files(file_name=name,date_time =datetime.date,audio_file=path)
   #   podcast.save()
     clips = audio.objects.all()
     podcasts = podcast_files.objects.all()
     return render(request,"merge.html",{'clips':clips,'podcasts':podcasts})

def pdf_upload(request):
  if request.method == "POST":
    file = request.FILES['pdf']
    pdfFileObj = open(file, "rb")
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    mytext = ""

    for pageNum in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)
        mytext += pageObj.extractText()

    pdfFileObj.close()

    # return mytext
    return render(request,"pdftotextdetail.html",{'text':mytext})
  

def readexcelfile(request):
   if request.method == "POST":
     file = request.FILES['excel']
    #  import os
    #  output_path = os.path.join(settings.BASE_DIR, f'media/excel/{file}')
     excels = excel_files(excel_file=file)
     excels.save()
    #  rd=pd.read_excel(f'media/excel/{file}')
    #  print(rd)
     import openpyxl 
     from openpyxl import Workbook
     from openpyxl.styles import Alignment
     dataframe = openpyxl.load_workbook(f'media/excel/{file}')
     
     dataframe1 = dataframe.active
     excel_data = list()

     for row in dataframe1.iter_rows():
        row_data=list()
        for cell in row:
            row_data.append(str(cell.value))
        excel_data.append(row_data)
    #  excel_data.append("</speak>")
    #  print(row_data)

     import os
    #  pt="media\excel\\"
     pt=os.path.join(BASE_DIR, 'media/',"excel//")
     print(pt)     
     for files_name in os.listdir(pt):
        file =pt+files_name
        if os.path.exists(file):
            print("Deleting file")
            os.remove(file)
    

   return render(request,"exceltotextdetail.html",{'excel_data':excel_data})

def readexcel(request):

   return render(request,"exceltotext.html")


def convert(request):
 if request.method == "POST":
     name  = request.POST.get('filename')
     text = request.POST.get('script')
     path= convert_text_to_audio(text,name)
     Audio= audio(file_name=name,date_time= datetime.date ,audio_file=path)
    #  Audio= audio(file_name=name)
     Audio.save()
   
 return render(request,"home.html")

