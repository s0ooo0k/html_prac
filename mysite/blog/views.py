from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .forms import CommentForm

# Create your views here.

def home(request):
    blogs=Blog.objects
    return render(request, 'home.html', {'blogs':blogs})

def detail(request, blog_id):
    blog_detail=get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'blog':blog_detail})

def new(request):
    return render(request, 'new.html')

def create(request):
    blog=Blog()
    blog.title=request.GET['title']
    blog.body=request.GET['body']

    blog.pub_date=timezone.datetime.now()
    blog.save()
    return redirect('/blog/' + str(blog.id))

def delete(request, blog_id):
    blog=Blog.objects.get(pk=blog_id)
    blog.delete()
    return redirect('home')

def edit(request, blog_id):
    blog_edit=Blog.objects.get(pk=blog_id)
    return render(request, 'edit.html', {'blog':blog_edit})

@csrf_exempt
def update(request, blog_id):
    blog=Blog.objects.get(pk=blog_id)
    blog.title=request.POST['title']
    blog.body=request.POST['body']
    blog.pub_date=timezone.datetime.now()
    blog.save()
    return redirect('home')

def add_comment_to_post(request, blog_id):
    blog=get_object_or_404(Blog, pk=blog_id)
    if request.method =="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=blog
            comment.save()
            return redirect('blog:detail', blog_id)
    else:
        form=CommentForm()
    return render(request, 'add_comment_to_post.html', {'form':form})