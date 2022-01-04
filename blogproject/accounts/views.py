from django.shortcuts import render, redirect
from django.contrib import auth # 유저가 DB에 있는지 없는지 or 로그인, 로그아웃 수행
from django.contrib.auth.models import User
def login(request):
    # POST 요청이 들어오면 로그인 처리를
    if request.method == 'POST' :
        userid = request.POST['username']
        pwd = request.POST['password']
        user = auth.authenticate(request, username=userid, password=pwd) # 있으면 User 반환, 없으면 None 반환
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html')

    # GET 요청이 들어오면 longin form을 담고있는 login.html을 띄워주는 역할
    else :
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')