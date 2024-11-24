import os
from django.core.exceptions import ValidationError

def validate_file_type_and_size(file):
  #check the file type
  if not file.name.endswith('.pdf'):
    raise ValidationError('Only PDF files are allowed.')
  
  #check the file size
  file_size = file.size
  max_size = 5 * 1024 * 1024 #5MB in bytes
  if file_size > max_size:
    raise ValidationError('File size cannot exceed 5MB.')