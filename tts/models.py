from django.db import models

class audio(models.Model):
    file_name= models.CharField(max_length=40)
    date_time=models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to='recs',
        blank=True, null=True)
    
    def __str__(self):
        return self.file_name
    
class podcast_files(models.Model):
    file_name= models.CharField(max_length=60)
    date_time =models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to='podcast',
        blank=True, null=True)
    
    def __str__(self):
        return self.file_name
    
class excel_files(models.Model):
    excel_file = models.FileField(upload_to='excel')
    
def __str__(self):
        return self.file_name
    

