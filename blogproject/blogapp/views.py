from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from django.utils import timezone
from .forms import BlogForm, BlogModelForm, CommentForm

def home(request) :
    # 블로그 글들을 모두 띄워주는 코드
    posts = Blog.objects.all()
    # 날짜 내림차순 필터해서 가져오고 싶은 경우 : posts = Blog.objects.fliter().order.by('-date')
    return render(request,'index.html', {'posts':posts})

# 블로그 글 작성 html을 보여주는 함수
def new(request) :
    return render(request,'new.html')

# 블로그 글을 저장해주는 함수
def create(request) :
    if(request.method == 'POST'):
        post = Blog()
        post.tilte = request.POST['title']
        post.body = request.POST['body']
        post.date = timezone.now()
        post.save()
    return redirect('home')

# django form을 이용해서 입력값을 받는 함수
# GET 요청과 (= 입력값을 받을 수 있는 html을 갖다 줘야함)
# POST 요청 (= 입력한 내용을 데이터베이스에 저장. form에서 입력한 내용 처리)
# 둘 다 처리가 가능한 함수
def formcreate(request):
    if request.method =='POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            post = Blog()
            post.title = form.cleaned_data['title']
            post.body = form.cleaned_data['body']
            post.save()
            return redirect('home')
        # 입력 내용을 DB에 저장
    else:
        # 입력을 받을 수 있는 html을 갖다주기
        form = BlogForm()
    return render(request, 'form_create.html', {'form':form})

def modelformcreate(request):
    if request.method =='POST' or request.method == 'FILES':
        form = BlogModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        # 입력 내용을 DB에 저장
    else:
        # 입력을 받을 수 있는 html을 갖다주기
        form = BlogModelForm()
    return render(request, 'form_create.html', {'form':form})

def detail(request, blog_id):
    # blog_id 번째 블로그 글을 데이터베이스로부터 갖고와서
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    # blog_id 번째 블로그 글을 datail.html로 띄워주는 코드

    comment_form = CommentForm()
    return render(request, 'detail.html', {'blog_detail':blog_detail,'comment_form':comment_form})

def create_comment(request, blog_id):
    filled_form = CommentForm(request.POST)

    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False)
        finished_form.post = get_object_or_404(Blog, pk=blog_id)
        finished_form.save()
        # 아직 저장하지 마라는 명령하고 새 변수에 담아준 뒤 post에 블로그 아이디 담고 저장하는 논리 중요

    return redirect('detail',  blog_id)