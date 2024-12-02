from django.db import models
from pc.models import SubmissionBin
from dean.models import CustomUser, Department, Program
from .validators import validate_size


# Create your models here.


class Document(models.Model):

  
  submission_bin = models.ForeignKey(SubmissionBin, on_delete=models.CASCADE)
  submitted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  file = models.FileField(upload_to='documents/', validators=[validate_size])
  date_submitted = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=30, choices=[('Pending','Pending'),('Approved','Approved'),('Declined','Declined')])
  comment = models.TextField(blank=True, null=True)
  document_type = models.CharField(max_length=100)
  document_name = models.CharField(max_length=255)
  department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
  program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
  
