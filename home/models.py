from django.db import models

# Create your models here.


class PDFUploader(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/')
    # uploaded_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"PDFUploader(id={self.id}, file='{self.file.name}', uploaded_at='{self.uploaded_at}')"
