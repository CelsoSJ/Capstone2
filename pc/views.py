from django.shortcuts import render,redirect, get_object_or_404
from .forms import SubmissionBinForm, EditSubmissionBinForm
from dean.models import CustomUser,Program
from faculty.models import Document
from .models import Notification, SubmissionBin
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
# Create your views here.

def homepage(request):
  return render(request, 'pc/homepage.html')

def submission(request):
  user_bins = SubmissionBin.objects.filter(created_by=request.user).order_by('-date_created') # get bins created by the user
  return render(request, 'pc/Submission.html', {'user_bins':user_bins})



def create_submission_bin(request):
    if request.method == 'POST':
        form = SubmissionBinForm(request.POST)
        if form.is_valid():
            submission_bin = form.save(commit=False)
            submission_bin.created_by = request.user
            submission_bin.department = request.user.department

            # hay kapagal san many to many field
            # this get the first program associated with the user, but the program chair only has one program 
            #user_programs = request.user.program.all()
           # for program in user_programs:
               #user_program = get_object_or_404(Program, id=program.id)
              # submission_bin.program = user_program

            #user_programs = request.user.program.all()
            #if user_programs.exists():
             #  program_instance = user_programs.first()
              # submission_bin.program = program_instance

            user = get_object_or_404(CustomUser, id=request.user.id)
            get_user_program = user.program.all()
            getProgramId = get_user_program.first()

            program_id = getProgramId.id
            program = Program.objects.get(id=program_id)
            submission_bin.program = program

            submission_bin.save()
            
            notify_users(f"New submission Bin for '{submission_bin.academic_year} - {submission_bin.semester}' was created", user_role_id=1,program=program_id)  #notify faculty users whenever a new submission bin was created
            messages.success(request, 'Submission Bin created successfully!')
            return JsonResponse({"success": True})
        
        else:
           print(f"Form errors: {form.errors}")
           html_form = render_to_string('pc/create_submission_bin.html',{'form':form}, request=request)
           return JsonResponse({'success':False, 'html_form':html_form})
    else:
       form = SubmissionBinForm()
       return render(request,'pc/create_submission_bin.html', {'form':form})
    



def edit_submission_bin(request,user_bin_id):
    bin = get_object_or_404(SubmissionBin, id=user_bin_id)
    if request.method == 'POST':
        form = EditSubmissionBinForm(request.POST, instance=bin)
        if form.is_valid():
            form.save()
            #notify_users(f"New submission Bin for '{submission_bin.academic_year} - {submission_bin.semester}' was created", user_role_id=1,program=request.user.program)  #notify faculty users whenever a new submission bin was created
            messages.success(request, 'Submission Bin was successfully edited!')
            return JsonResponse({"success": True})
        
        else:
           html_form = render_to_string('pc/edit_submission_bin.html',{'form':form, 'bin': bin}, request=request)
           return JsonResponse({'success':False, 'html_form':html_form})
    else:
       form = EditSubmissionBinForm(instance=bin)
    
    return render(request, 'pc/edit_submission_bin.html', {'form': form, 'bin':bin})
    




# function for creating a notification  after creating submission bin this will notify the faculty
def notify_users(message,user_role_id, program):
  users = CustomUser.objects.filter(role_id=user_role_id).filter(program=program)
  for user in users:
    Notification.objects.create(receipient=user, message=message)






def documents_for_review(request, submission_bin_id):
   submission_bin = get_object_or_404(SubmissionBin, id=submission_bin_id) #get submission_bin_id
   documents = Document.objects.filter(submission_bin=submission_bin).filter(status="Pending").order_by('-date_submitted')  #get all documents submitted in a specific submission_bin in descending order
   return render(request, 'pc/documents_for_review.html', {'submission_bin':submission_bin, 'documents':documents})



def confirm_approve_document(request,document_id):
   document = get_object_or_404(Document, id=document_id)
   submission_bin_id = document.submission_bin.id
   document.status = "Approved"
   document.save()

   #displays a one-time notification on the page after approving the document
   messages.success(request, f'Document {document.document_name} has been approved successfully!')


   #create a record in the notification model
   Notification.objects.create(
      user=document.submitted_by, 
      message= f'Your document "{document.document_name}" has been approved!'
   )
   return redirect(reverse('documents-for-review', args=[submission_bin_id]))  #the system will direct the user to the documents_for_review page after approving the document.
   


def confirm_decline_document(request, document_id):
   if request.method == "POST":
     comment = request.POST.get('comment')
     document = get_object_or_404(Document, id=document_id)
     submission_bin_id = document.submission_bin.id 
     document.status = "Declined"
     document.comment = comment
     document.save()

   #Creates a one-time notif after declining the document
     messages.success(request, f'Document "{document.document_name}" has been declined.')

   #Creates a record in the Notification model after decling the document
     Notification.objects.create(
      user = document.submitted_by,
      message= f'Your document "{document.document_name}" has been declined.'
   )

     return redirect(reverse('documents-for-review', args=[submission_bin_id]))  #the system will direct the user to the documents_for_review page after declining the document.






def view_facultyFiles(request):
  approved_files = Document.objects.filter(program=request.user.program).filter(status='Approved')
  declined_files = Document.objects.filter(program=request.user.program).filter(status='Declined')
  return render(request, 'pc/Files.html', {'approved_files':approved_files, 'declined_files':declined_files})




# view for viewing pc notifications
def pc_notification_list(request):
  notifications = Notification.objects.filter(receipient=request.user).order_by('-date_created')
  return render(request, 'pc/notification.html', {'notifications':notifications})


# view for changing the read attribute of notification to true
def mark_as_read(request, notification_id):
  notification = get_object_or_404(Notification, id=notification_id)
  notification.read = True
  notification.save()
  return redirect('pc-notifications')


#view for counting unread notification
def unread_notification_count(request):
  unread_count = Notification.objects.filter(receipient=request.user).filter(read=False).count()
  return JsonResponse({'unread_count':unread_count})

