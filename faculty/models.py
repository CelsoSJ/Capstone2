from django.db import models
from pc.models import SubmissionBin
from dean.models import CustomUser, Department, Program
from .validators import validate_file_type_and_size


# Create your models here.


class Document(models.Model):

  DOCUMENT_TYPE_CHOICES = [
    ('Personal Data Sheet','Personal Data Sheet'),
    ('Syllabi','Syllabi'),
    ('Class Records','Class Records'),
    ('Grading Sheets', 'Grading Sheets'),
    ('Accomplishment Report','Accomplishment Report'),
    ('Exams','Exams'),
    ('Quizzes/Tests','Quizzes/Tests'),
    ('Table of Specifications','Table of Specifications'),
    ('Rubrics','Rubrics'),
    ('Sample Student Project','Sample Student Project'),
    ('Instructional Materials','Instructional Materials'),
    ('PRC License','PRC License'),
    ('Trainings/Seminars','Trainings/Seminars'),
    ('Research Projects','Research Projects'),
    ('Extension Projects','Extension Projects'),
    ('Documentation','Documentation'),
    ('Membership in Organization','Membership in Organization')
  ]

  submission_bin = models.ForeignKey(SubmissionBin, on_delete=models.CASCADE)
  submitted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  file = models.FileField(upload_to='documents/', validators=[validate_file_type_and_size])
  date_submitted = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=30, choices=[('Pending','Pending'),('Approved','Approved'),('Declined','Declined')])
  comment = models.TextField(blank=True, null=True)
  document_type = models.CharField(max_length=100, choices=DOCUMENT_TYPE_CHOICES)
  document_name = models.CharField(max_length=255)
  department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
  program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
