from django.shortcuts import render, redirect
from .models import Post, PostAttachment

def post_list(request):
    posts = Post.objects.all()
    context = {
        'post_list':posts,
    }
    return render(request, 'posts/post_list.html', context)

def post_detail(request,pid):
    post = Post.objects.get(pk = pid)
    post_attachmments = post.images.all()
    context = {
        'post':post,
        'post_attachmments':post_attachmments
    }
    return render(request, 'posts/post_detail.html', context)

from .forms import PostForm
from django.contrib.auth.decorators import login_required

@login_required
def post_new(request):
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(request.POST)
        attachments = request.FILES.getlist('images')
        if form.is_valid():
            post:Post = form.save(commit=False)
            post.author = request.user
            post.save()
            for att in attachments:
                obj = PostAttachment.objects.create(
                    image = att
                )
                post.images.add(obj)
            return redirect('post_detail', pid = post.pk)
    context = {
        'form':form
    }
    return render(request, 'posts/post_new.html', context)

def post_edit(request,pid):
    post = Post.objects.get(pk=pid)
    if not request.user.is_authenticated or request.user != post.author:
        return redirect('/')
    post_att = post.images.all()
    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(request.POST,instance=post)
        attachments = request.FILES.getlist('images')
        if form.is_valid():
            post:Post = form.save(commit=False)
            post.author = request.user
            post.save()
            for att in attachments:     #NOTE - Тут происходит создание объектов для приложений поста
                obj = PostAttachment.objects.create(
                    image = att
                )
                post.images.add(obj)
            chosen = request.POST.getlist('attachments')
            for image_id in chosen:
                PostAttachment.objects.get(pk=int(image_id)).delete()
            print(chosen)
            return redirect('post_detail', pid = post.pk)
    context = {
        'form':form,
        'post_att':post_att
    }
    return render(request, 'posts/post_edit.html', context)