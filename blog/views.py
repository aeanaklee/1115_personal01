from django.shortcuts import redirect, render, get_object_or_404, redirect
from .models import Blog, Comment, HashTag
from django.utils import timezone
from .forms import BlogForm, CommentForm
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
import json
# Create your views here.


def home(request):
    blog = Blog.objects.order_by('-pub_date')  # query set!
    return render(request, 'home.html', {'blogs': blog})


def all_list(request):
    blog = Blog.objects.order_by('-pub_date')  # query set!
    return render(request, 'all_list.html', {'blogs': blog})


def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    blog_hashtag = blog_detail.hashtag.all()
    return render(request, 'detail.html', {'blog': blog_detail, 'hashtags': blog_hashtag})


def new(request):
    form = BlogForm()
    return render(request, 'new.html', {'form': form})


def create(request):
    form = BlogForm(request.POST, request.FILES)
    if form.is_valid():
        new_blog = form.save(commit=False)
        new_blog.pub_date = timezone.now()
        new_blog.writer = request.user
        new_blog.save()
        hashtags = request.POST['hashtags']
        hashtag = hashtags.split(",")
        if 'image' in request.FILES:
            image = request.FILES['image']
        for tag in hashtag:
            ht = HashTag.objects.get_or_create(hashtag_name=tag)
            new_blog.hashtag.add(ht[0])
        return redirect('detail', new_blog.id)
    return redirect('home')


def edit(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'edit.html', {'blog': blog_detail})


def update(request, blog_id):
    blog_update = get_object_or_404(Blog, pk=blog_id)
    blog_update.title = request.POST['title']
    blog_update.body = request.POST['body']
    if 'image' in request.FILES:
        blog_update.image = request.FILES['image']
    blog_update.save()
    return redirect('detail', blog_id)


def delete(request, blog_id):
    blog_delete = get_object_or_404(Blog, pk=blog_id)
    blog_delete.delete()
    return redirect('home')


def add_comment_to_post(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author_name = request.user
            comment.post = blog
            comment.save()
            return redirect('detail', blog_id)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})


def delete_comment(request, blog_id, comment_id):  # ?????? ????????????
    comment_delete = Comment.objects.get(id=comment_id)
    comment_delete.delete()
    return redirect('detail', blog_id)


def edit_comment(request, blog_id, comment_id):  # ?????? ????????????
    comment = Comment.objects.get(id=comment_id)
    return render(request, 'edit_comment.html', {'comment': comment})


def update_comment(request, comment_id):
    comment_update = Comment.objects.get(id=comment_id)
    comment_update.comment_text = request.POST['comment_text']
    comment_update.save()
    return redirect('home')


def cate01(request):
    blogs = Blog.objects.all().filter(category_id=1).order_by('-pub_date')
    return render(request, 'cate01.html', {'blogs': blogs})


def cate02(request):
    blogs = Blog.objects.all().filter(category_id=2).order_by('-pub_date')
    return render(request, 'cate02.html', {'blogs': blogs})


def search(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        hashtag = HashTag.objects.filter(hashtag_name=keyword)
        blog = Blog.objects.filter(hashtag__in=hashtag).order_by('-pub_date')
        return render(request, 'search.html', {'blogs': blog, 'keyword': keyword})
    elif request.method == 'GET':
        return redirect('/')


def search01(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        hashtag = HashTag.objects.filter(hashtag_name=keyword)
        blog = Blog.objects.filter(
            hashtag__in=hashtag, category_id=1).order_by('-pub_date')
        return render(request, 'Search01.html', {'blogs': blog, 'keyword': keyword})
    elif request.method == 'GET':
        return redirect('/')


def search02(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        hashtag = HashTag.objects.filter(hashtag_name=keyword)
        blog = Blog.objects.filter(
            hashtag__in=hashtag, category_id=2).order_by('-pub_date')
        return render(request, 'Search01.html', {'blogs': blog, 'keyword': keyword})
    elif request.method == 'GET':
        return redirect('/')


def mypage(request):
    myblog = Blog.objects.filter(writer=request.user)
    user_info = request.user
    user_like = request.user.likes.all()
    return render(request, 'mypage.html', {'myblogs': myblog, 'user_infos': user_info, 'user_likes': user_like, })


def likes(request):
    if request.is_ajax():  # ajax ????????? ??? ?????? ?????? ??????
        blog_id = request.GET['blog_id']  # ???????????? ?????? ?????????id (blog_id)????????? ??????
        post = Blog.objects.get(id=blog_id)

        if not request.user.is_authenticated:  # ????????? ?????? ????????? ???????????? ????????? ???
            message = "????????? ?????????"  # ????????? ?????? ?????????
            context = {'like_count': post.like.count(), "message": message}
            return HttpResponse(json.dumps(context), content_type='application/json')

        user = request.user  # request.user : ?????? ???????????? ??????
        if post.like.filter(id=user.id).exists():  # ?????? ???????????? ?????? ????????? ???
            post.like.remove(user)  # like field??? ?????? ?????? ??????
            message = "???????????? ??????"  # ????????? ?????? ?????????
        else:  # ???????????? ????????? ?????? ????????? ???
            post.like.add(user)  # like field??? ?????? ?????? ??????
            message = "???????????? ??????"  # ????????? ?????? ?????????
        # post.like.count() : ???????????? ?????? ????????? ???
        context = {'like_count': post.like.count(), "message": message}
        return HttpResponse(json.dumps(context), content_type='application/json')
