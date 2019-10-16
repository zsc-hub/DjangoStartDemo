from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserInfo, UserProfile
from .forms import LoginForm,RegistrationForm,UserProfileForm,UserForm,UserInfoForm

# Create your views here.
# 个人信息编辑
@login_required(login_url='../login/')
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user)

    if request.method == 'POST':
        user_from = UserForm(request.POST)
        userprofile_from = UserProfileForm(request.POST)
        userinfo_from = UserInfoForm(request.POST)
        print("request.POST:{}".format(request.POST))
        if user_from.is_valid() or userprofile_from.is_valid() or userinfo_from.is_valid():
            print("*****")
            user_cd = user_from.data
            userprofile_cd = userprofile_from.data
            userinfo_cd = userinfo_from.data
            user.email=user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('../my-information')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth":userprofile.birth, "phone":userprofile.phone})
        userinfo_form = UserInfoForm(initial={"school":userinfo.school, "company":userinfo.company, "profession":userinfo.profession, "address":userinfo.address, "aboutme":userinfo.aboutme})
        return render(request,'account/myself_edit.html', {"user_form":user_form, "userprofile_form":userprofile_form, "userinfo_form":userinfo_form})
# 个人信息展示页面
@login_required(login_url="../login")   # 只有登录才能看到，如果没有登录则指向登录页面
def myself(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    return render(request, "account/myself.html", {"user":user, "userprofile":userprofile, "userinfo":userinfo})


# 登录方法
def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                # 地址的重定向都是在原有的地址基础上拼接上参数中的地址来实现的
                return HttpResponseRedirect("../my-information")
            else:
                return HttpResponse("Sorry. your username or password is not right")

        else:
            return HttpResponse("Invalid login")

    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "account/login.html", {"form":login_form})

def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.data["password"])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user=new_user)
            return HttpResponse("successfully")
        else:
            return HttpResponse("sorry, you can not register")
    else:
        user_form = RegistrationForm()
        user_profile = UserProfileForm()
        return render(request, "account/register.html", {"form":user_form, "profile":user_profile})