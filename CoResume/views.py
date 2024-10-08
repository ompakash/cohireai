import os
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
import PyPDF2
from django.conf import settings

class ResumePDFUpload(APIView):
    def post(self, request):
        # Ensure the media directory exists
        media_dir = os.path.join(settings.MEDIA_ROOT, settings.APPS_MEDIA_DIRS['resumeapp'])
        os.makedirs(media_dir, exist_ok=True)

        if 'pdf_file' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        pdf_file = request.FILES['pdf_file']
        
        # Save the PDF file
        pdf_document = ResumePDFDocument()
        pdf_document.pdf_file.save(pdf_file.name, pdf_file)

        # Extract text from the PDF
        text = self.extract_text_from_pdf(pdf_document.pdf_file.path)
        pdf_document.extracted_text = text
        pdf_document.save()

        # Prepare the response data
        response_data = {
            'id': pdf_document.id,
            'pdf_file': pdf_document.pdf_file.url,
            'extracted_text': pdf_document.extracted_text,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def extract_text_from_pdf(self, file_path):
        text = ''
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ''
        return text
