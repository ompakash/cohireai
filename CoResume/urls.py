# pdfapp/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('upload_resume/', ResumePDFUpload.as_view(), name='upload_resume'),
]
