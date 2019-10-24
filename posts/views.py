from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'posts/index.html', context)

@login_required
def create(request):
    # 여기서 post 가지고 왔는지 기억이 안나네..
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # form.save()
            #여기는 바로 save가 안 돼..
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("posts:index") #여기도 detail로 바로 갔는지 기억이 안남...
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/form.html', context)

def detail(request, id):
    post = get_object_or_404(Post, id=id)
    form = CommentForm()
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'posts/detail.html', context)

@login_required
def update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        if post.user == request.user:
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('posts:detail', id)
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, 'posts/form.html', context)

@login_required
def delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        if post.user == request.user:
            post.delete()
            return redirect('posts:index')

@login_required
def comment_create(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.post = post # 이게 뭐지..
            form.save()
            return redirect('posts:detail', id)
# 기억 안 남
@login_required
def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        if comment.user == request.user:
            comment.delete()
        return redirect("posts:detail", post_id)

@login_required
def like(request, id):
    post = get_object_or_404(Post, id=id)
    user = request.user

    if post.like_users.filter(id=user.id):
        post.like_users.remove(user)
    else:
        post.like_users.add(user)


    return redirect('posts:detail', id)
