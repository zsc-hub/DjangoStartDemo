#enconding=utf-8
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile,UserInfo

# 登录表单
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# 注册表单
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    """
        1.Meta(单词一定要拼写正确)是RegistrationForm的一个内部类
        2.RegistrationForm()对象有很多的属性，例如：['as_p', 'fields',...] 可通过dir(RegistrationForm())来查看
        3.可以通过该内部类来修改属性值，例如：fields = ("username", "email")
    """
    class Meta:
        # 设置model（单词拼写要正确）值，可以理解为引用已有的model即User
        model = User
        fields = ("username", "email")
        # fields = "__all__"

    def clean_password2(self):
        cd = self.data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("password do not match!")
        return cd["password2"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'birth')


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('school', 'company', 'profession', 'address', 'aboutme')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)

