from django.shortcuts import render,redirect, get_object_or_404
from .models import CustomUser,Department,Role,Program
from .forms import CustomUserCreationForm,CustomUserEditForm
from django.template.loader import render_to_string
from django.http  import JsonResponse
from django.contrib.auth.decorators import login_required #to enforce constraint to views
from django.contrib import messages  #built-in system that allows you to display one-time notifications to your users. It's a way to provide feedback to users after they've performed a certain action, such as submitting a form, deleting an object, or logging in.
from django.db.models import Q  #for complex queries, used in search functionality

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

# view for creating users
@login_required
def create_user(request):
  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST, dean=request.user)
    if form.is_valid():
      form.save()
      messages.success(request, 'User succesfully created!') #show alert after a new user is created
      return JsonResponse({'success':True})
    
    else:
      # #is used to render a Django template into a string, which is then returned as part of a JSON response. This is particularly useful in AJAX requests where you want to update part of a web page without a full page reload.
      form_html = render_to_string('dean/userManagement.html',{'form':form}, request=request)
      return JsonResponse({'success':False, 'form_html':form_html})
  
  return JsonResponse({'success':False, 'form_html': 'Invalid Request'})
  


#view for editing user info
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