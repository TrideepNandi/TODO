from django.shortcuts import render, get_object_or_404
from .models import Tasks
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render,redirect, HttpResponseRedirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.views import View
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import TasksForm  # Import the TasksForm

# Create your views here.

@login_required(login_url="/login")
def starting_page(request):
    latest_posts = Tasks.objects.filter(author=request.user).order_by("due_date")[:3] #select * from tasks where author = request.user order by due_date
    return render(request, "blog/index.html", {
      "posts": latest_posts
    })

@login_required(login_url="/login")
def posts(request):
    all_posts = Tasks.objects.filter(author = request.user).order_by("due_date")
    return render(request, "blog/all-posts.html", {
      "all_posts": all_posts
    })

@login_required(login_url="/login")
def post_detail(request, slug):
    identified_post = get_object_or_404(Tasks, slug=slug)
    return render(request, "blog/post-detail.html", {
      "post": identified_post,
    })

def login(request):
   if request.method=='POST':
      username=request.POST['username']
      password=request.POST['password']
      
      user=auth.authenticate(username=username,password=password)
      
      if user is not None:
         auth.login(request,user)
         return redirect("/")
      else:
         messages.error(request,'INVALID Credentials')
         return redirect('login')
   else:
      return render(request,'registration/login.html')  

class RegisterView(View):
    def get (self, request):
          return render (request, 'blog/register.html')
    
    def post (self, request):
        username = request.POST.get('username') 
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return HttpResponseRedirect("/signup")  
        else:
            user = User(username = username, email = email, password = password)
            user.save()
            auth_login(request, user)
            messages.success(request, f'Account created and logged in for {username}')
            return redirect('/')
          
@login_required(login_url="/login")
def create_task(request):
    if request.method == 'POST':
        form = TasksForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            return redirect('/')  # Redirect to the task list view after creating a task
    else:
        form = TasksForm()
    
    return render(request, 'blog/task_form.html', {'form': form})
  
def complete_task(request, slug):
    identified_post = get_object_or_404(Tasks, slug=slug)

    if request.method == 'POST':
        complete_task_value = request.POST.get('complete_task')
        if complete_task_value == 'true':
            identified_post.is_completed = True
        else:
            identified_post.is_completed = False
        identified_post.save()

    return redirect('post-detail-page', slug=slug)

def completed_tasks(request):
    completed_tasks = Tasks.objects.filter(is_completed=True).filter(author= request.user)
    return render(request, 'blog/completed_tasks.html', {'completed_tasks': completed_tasks})

def delete_task(request, slug):
    task = get_object_or_404(Tasks, slug=slug)

    if request.method == 'POST':
        task.delete()  # Hard delete the task
        return redirect('starting-page')

    return redirect('post-detail-page', slug=slug)
