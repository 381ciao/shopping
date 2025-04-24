from django import forms

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import CaptchaModel


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=10,min_length=2,error_messages={
        'required': "输入用户名",
        'max_length':"用户名长度在2~10之间",
        'min_length': "用户名长度在2~10之间",
    })
    email = forms.EmailField(error_messages={
        'required':"输入邮箱",
        'invalid':"请输入正确邮箱"
    })
    password = forms.CharField(max_length=18,min_length=6,error_messages={
        'required': "输入密码",
        'max_length': "密码长度在6~18之间",
        'min_length': "密码长度在6~18之间",
    })
    captcha = forms.CharField(max_length=4)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if  exists:
            raise forms.ValidationError('邮箱已经被注册！')
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')

        captchamodel = CaptchaModel.objects.get(email=email, captcha=captcha)
        if not captchamodel:
            raise forms.ValidationError('验证码和邮箱不匹配！')
        captchamodel.delete()
        return captcha

