from django.shortcuts import render
from faculty.models import Document
from django.db.models import Q
from dean.decorators import role_required


# Create your views here.

@role_required('Quality Assurance Officer')
def home_page(request):
  return render(request, 'qao/homepage.html')



@role_required('Quality Assurance Officer')
def all_files(request):

  #get all approved documents
  documents = Document.objects.all().filter(status="Approved")

  query = request.GET.get('search', '')
  # this filters the documents by search
  if query:
    documents = documents.filter(Q(document_type__icontains=query)| Q(submitted_by__username__icontains=query)| Q(program__name__icontains=query))


  cict_documents = documents.filter(department__name='CICT')
  cbme_documents = documents.filter(department__name='CBME')


  return render(request,'qao/files.html',{'cict_documents':cict_documents, 'cbme_documents':cbme_documents, 'query':query})