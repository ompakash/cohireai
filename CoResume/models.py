from django.db import models
from django.conf import settings

class ResumePDFDocument(models.Model):
    pdf_file = models.FileField(upload_to=f'{settings.APPS_MEDIA_DIRS["resumeapp"]}/') 
    extracted_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.pdf_file.name
