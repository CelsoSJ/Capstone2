import os
from django.core.exceptions import ValidationError

def validate_size(file):
  
  #check the file size
  file_size = file.size
  max_size = 20 * 1024 * 1024 #20MB in bytes
  if file_size > max_size:
    raise ValidationError('File size cannot exceed 20MB.')