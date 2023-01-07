import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from django.contrib.auth.models import User
from .models import Category, Task

# Create your views here.


class Authentication:
    def signup(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            password2 = request.POST['passwordverification']
            if password != password2:
                return render(request, 'authentication/signup.html', {
                    'passworderror' : 'Passwords do not match. Please try again.'
                })
            form = UserForm()
            if form.is_valid():
                user = User.objects.create()
                user.username = username
                user.email = request.POST['email']
                user.set_password(password)
                user.save()
                user = authenticate(usename=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')
            else:
                return render(request, 'authentication/signup.html', {
                    'internalerror' : 'There was a server error. Please try again.'
                })
        return render(request, 'authentication/signup.html')
    
    def loginuser(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'authentication/login.html', {
                    'error' : 'Invalid username or password.'
                })
        
        return render(request, 'authentication/login.html')
    
    def logoutuser(request):
        logout(request)
        return redirect('loginuser')
    

class Dashboard:    
    @login_required()
    def index(request):
        tasks = Task.objects.filter(category=1, user=request.user)
        timenow = datetime.date.today()
        return render(request, 'core/dashboard.html', {
            'time' : timenow,
            'tasks' : tasks,
            'category' : Category.objects.get(id=1),
        })
        
        
    @login_required()    
    def category(request, id):
        tasks = Task.objects.filter(category=id, user=request.user)
        return render(request, 'core/dashboard.html', {
            'tasks' : tasks,
            'category' : Category.objects.get(id=id),
        })
        
    @login_required()
    def alltasks(request):
        tasks = Task.objects.filter(user=request.user)
        return render(request, 'core/dashboard.html', {
            'tasks' : tasks,
            'category' : Category.objects.get(id=4)
        })
        
    @login_required()
    def importanttasks(request):
        tasks = Task.objects.filter(important=True, user=request.user)
        return render(request, 'core/dashboard.html', {
            'tasks' : tasks,
            'category' : Category.objects.get(id=2)
        })
    
    @login_required()
    def taskcheck(request, id, categoryid):
        task = Task.objects.get(id=id)

        if task.completed:
            task.completed = False
            
        else:
            task.completed = True
            
        task.save()
        
        if categoryid == 4:
            return redirect('alltasks')
        
        elif categoryid == 5:
            return redirect('completedtasks')
        
        elif categoryid == 2:
            return redirect('importanttasks')
        
        if categoryid == 1:
            return render(request, 'core/dashboard.html', {
            'time' : datetime.date.today(),
            'tasks' : Task.objects.filter(category=1, user=request.user),
            'category' : Category.objects.get(id=1),
            })
        
        else: 
            return render(request, 'core/dashboard.html', {
            'tasks' : Task.objects.filter(category=categoryid),
            'category' : Category.objects.get(id=categoryid),
            })

    @login_required()
    def completedtasks(request):
        tasks = Task.objects.filter(completed=True, user=request.user)
        return render(request, 'core/dashboard.html', {
            'tasks' : tasks,
            'category' : Category.objects.get(id=5),
        })
        
    @login_required()
    def addtask(request, categoryid):
        tasks = Task.objects.filter(category=categoryid, user=request.user)
        if request.method == 'POST':
            content = request.POST['content']
            if content == "":
                return render(request, 'core/dashboard.html', {
                'tasks' : tasks,
                'category' : Category.objects.get(id=categoryid),
                'message' : 'Task cannot be blank.',
                'messagetype' : 'danger',
            })

            Task.objects.create(content=content, user=request.user, category=Category.objects.get(id=categoryid))
            return render(request, 'core/dashboard.html', {
                'tasks' : tasks,
                'category' : Category.objects.get(id=categoryid),
                'message' : 'Task added.',
                'messagetype' : 'success',
            })
            
    @login_required()
    def deletetask(request, id, categoryid):
        task = Task.objects.get(id=id)
        task.delete()
        
        if categoryid == 4:
            return redirect('alltasks')
        
        if categoryid == 5:
            return redirect('completedtasks')
            
        tasks = Task.objects.filter(category=categoryid, user=request.user)
        return render(request, 'core/dashboard.html', {
            'tasks' : tasks,
            'category' : Category.objects.get(id=categoryid),
            'message' : 'Task deleted.',
            'messagetype' : 'danger',
        })

        
    @login_required()
    def importance(request, id, categoryid):
        task = Task.objects.get(id=id)
        if task.important:
            task.important = False
        else:
            task.important = True
            
        task.save()
        
        if categoryid == 4:
            return redirect('alltasks')
        
        if categoryid == 5:
            return redirect('completedtasks')
        
        
        tasks = Task.objects.filter(category=categoryid, user=request.user)
        return render(request, 'core/dashboard.html', {
            'tasks' : tasks,
            'category' : Category.objects.get(id=categoryid)
        })
