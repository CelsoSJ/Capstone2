from django.shortcuts import render, get_object_or_404, redirect #a utility function provided by Django that simplifies the process of retrieving an object from the database while handling the case where the object does not exist. It is commonly used in Django views to fetch a single object based on a given query, and it automatically raises a 404 Not Found error if the object is not found. This is particularly useful for improving user experience by providing a clear response when a requested resource is not available.
from django.contrib.auth.decorators import login_required
from dean.models import CustomUser
from pc.models import SubmissionBin, Notification
from .models import Document
from pc.views import notify_users
from .forms import DocumentForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from pc.models import Notification
# Create your views here.


@login_required
def home(request):
  return render(request,'faculty/home.html')

def files(request):
  user = CustomUser.objects.get(username=
  request.user)
  
  approved_documents = Document.objects.filter(submitted_by = user.id).filter(status="Approved").order_by('-date_submitted')

  declined_documents = Document.objects.filter(submitted_by = user.id).filter(status="Declined").order_by('-date_submitted')

  pending_documents = Document.objects.filter(submitted_by = user.id).filter(status="Pending").order_by('-date_submitted')

  return render(request,'faculty/Files.html',{'approved_documents':approved_documents, 'declined_documents':declined_documents, 'pending_documents':pending_documents})



def submissionBinList(request):
  #get user's department and program
  faculty_user = request.user
  department = faculty_user.department
  program = faculty_user.program.all()

  #filter submission bins by user's department and program
  submission_bins = SubmissionBin.objects.filter(department=department, program__in=program).order_by('-date_created')
  return render(request, 'faculty/submission_bin_list.html',{'submission_bins':submission_bins, 'program':program})






def submit_document(request, submission_bin_id):
  submission_bin = get_object_or_404(SubmissionBin, id=submission_bin_id)
  if request.method == 'POST':
    form = DocumentForm(request.POST,request.FILES)
    if form.is_valid():
      document = form.save(commit=False)
      document.submission_bin = submission_bin
      document.submitted_by = request.user
      document.status = 'Pending'
      document.save()
      #notify pc whenever new document was submitted
      notify_users(f"New document was submitted by '{request.user}'",receipient = submission_bin.created_by )
      messages.success(request, 'Document was successfully submitted!')
      return JsonResponse({"success": True})
    
    else:
      html_form = render_to_string('faculty/submit_document.html',{'form':form}, request=request)
      return JsonResponse({'success':False, 'html_form':html_form})
    
  else:
    form = DocumentForm()
    return render(request, 'faculty/submit_document.html',{'form':form, 'submission_bin':submission_bin})
  

#function for creating a notification record that will be saved in the database
def notify_users(message,receipient):
  Notification.objects.create(message=message, receipient=receipient)

  


# view for viewing faculty notifications
def faculty_notification_list(request):
  notifications = Notification.objects.filter(receipient=request.user).order_by('-date_created')
  return render(request, 'faculty/notifications.html', {'notifications':notifications})


# view for changing the read attribute of notification to true
def mark_as_read(request, notification_id):
  notification = get_object_or_404(Notification, id=notification_id)
  notification.read = True
  notification.save()
  return redirect('faculty-notifications')


#view for counting unread notification
def unread_notification_count(request):
  unread_count = Notification.objects.filter(receipient=request.user).filter(read=False).count()
  return JsonResponse({'unread_count':unread_count})

