# models.py
from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='resumes/')