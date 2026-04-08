from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PDFSerializer
from .models import PDFUploader

# Create your views here.


class PdfSummarizerAPI(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the PDF Summarizer API!"})
    
    def post(self, request):
        serializer = PDFSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)