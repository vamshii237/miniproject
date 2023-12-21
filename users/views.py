from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm

from blogs.models import Post

def register(request):
    if request.method == 'POST':
        print("in register")
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("valid")

            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created {username}! You are now able to log in')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def enotes(request):
    return render(request, "users/enotes.html")
def question(request):
    return render(request, "users/question.html")

@login_required
def profile(request):
    post = Post.objects.filter(author=request.user)
    post =post.order_by('-created_at')
    return render(request, "users/profile.html",{'object_list':post})

@login_required
def blogs_created(request):
    post = Post.objects.filter(author=request.user)
    post =post.order_by('-created_at')
    return render(request, 'users/created_blogs.html', {'object_list':post})



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Successfully Changed your details")
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})
