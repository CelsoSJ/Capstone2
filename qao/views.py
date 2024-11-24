from django.shortcuts import render

# Create your views here.

def home_page(request):
  return render(request, 'qao/homepage.html')


def all_files(request):
  return render(request,'qao/files.html')