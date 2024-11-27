from django.shortcuts import render
from faculty.models import Document


# Create your views here.

def home_page(request):
  return render(request, 'qao/homepage.html')


def all_files(request):
  documents = Document.objects.all().filter(status="Approved")
  return render(request,'qao/files.html',{'documents':documents})