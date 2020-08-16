from django.shortcuts import render, redirect, get_object_or_404
from .forms import JssForm, CommentForm
from .models import Jasoseol, Comment
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required # 데코레이터

# Create your views here.
def index(request):
    all_jss = Jasoseol.objects.all()
    return render(request, 'index.html', {'all_jss' : all_jss})

def my_index(request):
    my_jss = Jasoseol.objects.filter(author=request.user)
    # 자소설 오브젝트들 중에서 author 값이 현재 유저인 값만 전부 가져오기
    return render(request, 'index.html', {'all_jss' : my_jss})

@login_required(login_url='/login/')
def create(request):
    # if not request.user.is_authenticated:
    #     # 로그인하지 않은 사용자가 자소서를 작성하려고 할 경우
    #     return redirect('login')
    #     login_required 데코레이터로 대체 가능

    if request.method == "POST": # request가 넘겨준 값들이 POST 방식이면
        filled_form = JssForm(request.POST) # JssForm 객체를 request.POST 값으로 filled_form 변수에 저장
        
        if filled_form.is_valid(): # 값이 있으면 (유효성 검사)
            temp_form = filled_form.save(commit=False)
            temp_form.author = request.user
            # commit=False이면 폼(오브젝트)이 생성, 업데이트 되기 전에 임시 폼에 할당하면서 저장을 지연시키고 어떤 작업이 가능
            filled_form.save()
            return redirect('index')

    jss_form = JssForm()
    return render(request, 'create.html', {'jss_form' : jss_form})

@login_required(login_url='/detail/')
def detail(request, jss_id):
    # try:
    #    my_jss = Jasoseol.objects.get(pk=jss_id)
    # except:
    #    raise Http404 # 오브젝트가 없을 때 띄워주기 (get_object_or_404와 같음)
    my_jss = get_object_or_404(Jasoseol, pk=jss_id)
    comment_form = CommentForm()
    return render(request, 'detail.html', {'my_jss' : my_jss}, {'comment_form' : comment_form})

def delete(request, jss_id):
    my_jss = Jasoseol.objects.get(pk=jss_id)
    if request.user == my_jss.author:
        my_jss.delete()
        return redirect('index')

    raise PermissionDenied # 권한 거부

def update(request, jss_id):
    my_jss = Jasoseol.objects.get(pk=jss_id)
    jss_form = JssForm(instance=my_jss)

    if request.method == "POST":
        updated_form = JssForm(request.POST, instance='my_jss') # 값을 덮어쓰기 위해 instance 정해주기
        
        if updated_form.is_valid():
            updated_form.save()
            return redirect('index')

    return render(request, 'create.html', {'jss_form' : jss_form})

def create_comment(request, jss_id):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        temp_form = comment_form.save(commit=False)
        temp_form.author = request.user
        temp_form.jasoseol = Jasoseol.objects.get(pk=jss_id)
        temp_form.save()
        return redirect('detail', jss_id)

def delete_comment(request, jss_id, comment_id):
    my_comment = Comment.objects.get(pk=comment_id)
    if request.user == my_comment.author:
        my_comment.delete()
        return redirect('detail', jss_id)

    else:
        raise PermissionDenied
