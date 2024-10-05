from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.http import HttpResponseRedirect
from .forms import CommentForm

# List all posts
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

# View a single post
'''def post_detail(request, post_id):
   post = get_object_or_404(Post, id=post_id)
   comments = post.comments.all()
   return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})'''



# Create a new post
@login_required
def post_create(request):
    if request.method == 'POST':
        # Check if 'title' and 'content' are in request.POST
        title = request.POST.get('title')  # Use .get() to avoid MultiValueDictKeyError
        content = request.POST.get('content')
        
        # Ensure both title and content are provided
        if title and content:
            # Create the new post
            Post.objects.create(title=title, content=content, author=request.user)
            return redirect('post_list')  # Redirect to the post list after creation
        else:
            # Handle the case where title or content is missing
            return render(request, 'blog/post_form.html', {'error': 'Title and content are required.'})
    else:
        return render(request, 'blog/post_form.html')



# Edit a post
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Ensure that only the author can edit the post
    if post.author != request.user:
        return redirect('post_list')  # Or any other appropriate page

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)  # Redirect to the post detail page
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {'form': form, 'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Ensure that only the author can delete the post
    if post.author != request.user:
        return redirect('post_list')  # Or any other appropriate page

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')  # Redirect to the list of posts after deletion

    return render(request, 'blog/post_confirm_delete.html', {'post': post}) 



@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()  # Fetch all comments for the post

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('post_detail', pk=post.pk)  # Redirect to the same post after commenting
        else:
            return redirect('login')  # Redirect to login if the user is not authenticated

    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,  # Pass the form to the template
    })

