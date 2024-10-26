from django.shortcuts import render,redirect, get_object_or_404
from .models import CustomUser,Department,Role,Program
from .forms import CustomUserCreationForm,CustomUserEditForm
from django.template.loader import render_to_string
from django.http  import JsonResponse
from django.contrib.auth.decorators import login_required #to enforce constraint to views
from django.contrib import messages  #built-in system that allows you to display one-time notifications to your users. It's a way to provide feedback to users after they've performed a certain action, such as submitting a form, deleting an object, or logging in.
from django.db.models import Q  #for complex queries, used in search functionality
from django.contrib.auth import get_user_model  #returns the user model that is currently active in the project
from django.core.mail import send_mail  #Django's email handling module for sending emails
from django.utils.http import urlsafe_base64_encode ,urlsafe_base64_decode #function from django's utilities, useful for encoding/decoding data in a way that is safe to include in URLs
from django.utils.encoding import force_bytes, force_str  #essential for converting various data types into a bytes-like object, which is particularly useful when working with functions that require byte input, such as urlsafe_base64_encode.
from .tokens import account_activation_token  #importing the token that is created at tokens.py





# Create your views here
@login_required  #to restrict access to the view. It requires 
def home_page(request):
  return render(request, 'dean/homepage.html')

@login_required
def userManagement(request):
  exclude_roles = [3,4]
  query = request.GET.get('search', '')
  if query:
     users = CustomUser.objects.filter(Q(first_name__icontains=query)|Q(username__icontains=query) ).exclude(role__in=exclude_roles).exclude(is_staff=True)   #this search query will filter user with the first_name/username provided in the seach field
  else:
     users = CustomUser.objects.exclude(role__in=exclude_roles).exclude(is_staff=True) # this filters the list of users that will be rendered in the usermanagement page, so this excludes the Dean and QAO with an id of 3 and 4 respectively
  dean= request.user
  department = dean.department
  form = CustomUserCreationForm(dean=dean)
  return render(request, 'dean/UserManagement.html',{'users':users, 'form':form, 'department':department, 'query':query})


User = get_user_model()
# view for creating users
@login_required
def create_user(request):
  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST, dean=request.user)
    if form.is_valid():
      user = form.save(commit=False)
      user.is_active = False     #deactivate account until email verification
      user.save()

      #send verification email
      mail_subject = 'Activate your account.'
      message = render_to_string('dean/account_activation_email.html', {
         'user': user,
         'domain': request.META['HTTP_HOST'],
         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
         'token': account_activation_token.make_token(user),
      })
      send_mail(mail_subject, message, 'arikashikarimikutarimo@gmail.com', [user.email])


      messages.success(request, 'User succesfully created! An email has been sent for verification.') #show alert after a new user is created
      return JsonResponse({'success':True})
    
    else:
      # #is used to render a Django template into a string, which is then returned as part of a JSON response. This is particularly useful in AJAX requests where you want to update part of a web page without a full page reload.
      form_html = render_to_string('dean/userManagement.html',{'form':form}, request=request)
      return JsonResponse({'success':False, 'form_html':form_html})
  
  return JsonResponse({'success':False, 'form_html': 'Invalid Request'})
  


#a view for handling the activation link in the verification email
def activate(request, uidb64, token):
   try:
      uid = force_str(urlsafe_base64_decode(uidb64))
      user = User.objects.get(pk=uid)
   except(TypeError, ValueError, OverflowError, User.DoesNotExist):
      user = None

   if user is not None and account_activation_token.check_token(user, token):
      user.is_active = True
      user.save()
      return render(request, 'dean/activation_success.html')
   else:
      return render(request, 'dean/activation_invalid.html')
      





#view for editing user info
@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user, dean=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            form_html = render_to_string('dean/edit_user_form.html', {'form': form}, request=request)
            return JsonResponse({'success': False, 'form_html': form_html})
    else:
        form = CustomUserEditForm(instance=user, dean=request.user)
    return render(request, 'dean/edit_user_form.html', {'form': form, 'user':user})