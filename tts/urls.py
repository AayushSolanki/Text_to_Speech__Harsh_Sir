from django.urls import path
from . import views
app_name = 'tts'
urlpatterns = [
    path('', views.readexcel, name='read'),
    path('readexcel', views.readexcelfile, name='read'),
    path('mergedailogs', views.merge_dailogs, name='mergedailogs')
    # path('', views.CreatePDFView.as_view(), name='create-pdf'),
    # path('<int:pk>/details/', views.PDFDetailView.as_view(), name='pdf-detail'),
#    , path('merge/', views.mergeaudio, name='merge'),
    # # path('getclips/', views.getclips, name='getclips'),
    # path('convert', views.convert, name='convert'),
    # path('merge_files', views.merge_files, name='merge_files'),
    # path('pdf_upload', views.pdf_upload, name='script'),
    # path('script', views.script, name='script'),

    
    
    ]