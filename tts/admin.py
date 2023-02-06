from django.contrib import admin
from .models import audio, podcast_files

# class Audio(admin.ModelAdmin):
#     list_display = ('audio_file','file_name','date_time')
# admin.site.register(audio,Audio)


class Podcast(admin.ModelAdmin):
    list_display = ('audio_file','file_name','date_time')
admin.site.register(podcast_files,Podcast)

