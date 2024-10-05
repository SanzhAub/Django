from django.shortcuts import render, redirect, get_object_or_404, redirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Follow
from .forms import ProfileForm
from blog.models import Post

# User registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/registration.html', {'form': form})

# User profile
@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    return render(request, 'users/profile.html', {'profile': profile})

# Edit user profile
def profile_edit(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view', username=username)  # Redirect to the profile view after saving
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/profile_edit.html', {'form': form, 'profile_user': user})


@login_required
def profile_view(request, username):
    # Get the user by username
    user = get_object_or_404(User, username=username)
    
    # Get the associated profile
    profile = get_object_or_404(Profile, user=user)
    
    # Get the posts authored by the user
    posts = Post.objects.filter(author=user)

    # Check if the logged-in user is following the profile user
    is_following = Follow.objects.filter(follower=request.user, following=user).exists() if request.user.is_authenticated else False

    return render(request, 'users/profile.html', {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following  # Pass this variable to the template
    })

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.method == 'POST':
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile_view', username=username)  # Redirect to the followed user's profile

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    if request.method == 'POST':
        Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile_view', username=username)  

