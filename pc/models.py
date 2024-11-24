from django.db import models
from dean.models import CustomUser, Program, Department
from .validators import validate_deadline, validate_academic_year

# Create your models here.

class SubmissionBin(models.Model):
  SEMESTER_CHOICES = [
    ('1st Semester','1st Semester'),
    ('2nd Semester','2nd Semester'),
  ] # restricting the possible values for the semester at the model level, this is optional but recommended for data consistency


  semester = models.CharField(max_length=15, choices=SEMESTER_CHOICES, null=True)
  academic_year = models.CharField(max_length=9, validators=[validate_academic_year], null=True)
  description = models.TextField()
  created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_bins')
  date_created = models.DateTimeField(auto_now_add=True)
  deadline = models.DateTimeField(validators=[validate_deadline])
  program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True)
  department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)

  def __str__(self):
    return self.academic_year 



class Notification(models.Model):
  receipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notification')
  message = models.TextField()
  read = models.BooleanField(default=False)
  date_created = models.DateTimeField(auto_now_add=True)