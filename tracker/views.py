from django.shortcuts import render, get_object_or_404, redirect
from .models import Issue, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db.models import Q

def home(request):
    issues = Issue.objects.all().order_by('-created_at')
    query = request.GET.get('q')
    if query:
        issues = issues.filter(Q(title__icontains=query) | Q(description__icontains=query))

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter and status_filter != "ALL":
        issues = issues.filter(status=status_filter)

    # Filter by assigned user
    user_filter = request.GET.get('assigned_to')
    if user_filter and user_filter != "ALL":
        issues = issues.filter(assigned_to__id=user_filter)

    users = User.objects.all()
    return render(request, 'issue_list.html', {
        'issues': issues,
        'query': query,
        'status_filter': status_filter,
        'user_filter': user_filter,
        'users': users,
    })

def issue_detail(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    comments = issue.comments.all()
    return render(request, 'issue_detail.html', {'issue': issue, 'comments': comments})

@login_required
def issue_create(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        assigned_to = User.objects.filter(id=request.POST.get('assigned_to')).first()
        Issue.objects.create(title=title, description=description, assigned_to=assigned_to)
        return redirect('home')
    users = User.objects.all()
    return render(request, 'issue_form.html', {'users': users})

@login_required
def issue_edit(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == "POST":
        issue.title = request.POST['title']
        issue.description = request.POST['description']
        issue.status = request.POST['status']
        issue.assigned_to = User.objects.filter(id=request.POST.get('assigned_to')).first()
        issue.save()
        return redirect('home')
    users = User.objects.all()
    return render(request, 'issue_form.html', {'issue': issue, 'users': users})

@login_required
def issue_delete(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    issue.delete()
    return redirect('home')

@login_required
def add_comment(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == "POST":
        Comment.objects.create(issue=issue, author=request.user, text=request.POST['text'])
        return redirect('issue_detail', pk=pk)
    return redirect('issue_detail', pk=pk)


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username and password:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html', {'title':'Login'})

def logout(request):
    auth_logout(request)
    return redirect('login')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password, email=email)
        auth_login(request, user)
        return redirect('home')
    return render(request, 'register.html', {'title':'Register'})