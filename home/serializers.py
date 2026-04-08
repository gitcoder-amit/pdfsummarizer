from rest_framework import serializers
from .models import PDFUploader


class PDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFUploader
        fields = '__all__'