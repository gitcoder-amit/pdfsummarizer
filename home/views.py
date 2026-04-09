from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PDFSerializer
from .models import PDFUploader
from .utils import summarize_pdf
from django.conf import settings

# Create your views here.


class PdfSummarizerAPI(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the PDF Summarizer API!"})
    
    def post(self, request):
        serializer = PDFSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            actual_path = f"{settings.BASE_DIR}/pdfs/{serializer.validated_data['pdf_file'].name}"
            print('$$$$$$$$$$$$$$$')
            print(actual_path)
            data = summarize_pdf(actual_path)
            return Response({"summary": data}, status=201)
        return Response(serializer.errors, status=400)