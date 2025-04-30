from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import *
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm,UserAddressForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model,login,logout
from django.contrib import messages

User = get_user_model()
# Create your views here.
@require_http_methods(["GET", "POST"])
def account_login(request):
    if request.method == "GET":
        return render(request,'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                return redirect('/products/')
            else:
                print('郵箱或者密碼錯誤')
                return redirect(reverse('accounts:account_login'))

def account_logout(request):
    logout(request)
    return redirect('/')

@require_http_methods(['POST','GET'])
def account_register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('accounts:account_login'))
        else:
            print(form.errors)
            return render(request,'register.html',{'form':form})

def send_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code':400,'message':'必须传递邮箱！'})
    captcha = "".join(random.sample(string.digits,4))
    print(captcha)
    CaptchaModel.objects.update_or_create(email=email,defaults={'captcha':captcha})
    send_mail("SHOPPING网站注册",message=f"你的注册验证码是{captcha}",recipient_list=[email],from_email=None)
    return JsonResponse({'code':200,'message':'邮箱发送成功！'})

@login_required()
def address_list(request):
    # 查询数据
    # related_name='addresses'
    addresses = UserAddress.objects.all()
    return render(request,'address_list.html',{'addresses':addresses})

@login_required()
@require_http_methods(['POST','GET'])
def address_add(request):
    if request.method == 'GET':
        provinces = Region.objects.filter(level=1)
        return render(request, 'address_add.html',{'provinces':provinces})
    else:
        form = UserAddressForm(request.POST)
        if form.is_valid():
            receiver_name = form.cleaned_data.get('receiver_name')
            receiver_phone = form.cleaned_data.get('receiver_phone')
            # province = form.cleaned_data.get('province')
            # city = form.cleaned_data.get('city')
            # district = form.cleaned_data.get('district')
            detailed_address = form.cleaned_data.get('detailed_address')
            is_default = form.cleaned_data.get('is_default')

            # 获取地区对象
            province = get_object_or_404(Region, id=form.cleaned_data['province'])
            city = get_object_or_404(Region, id=form.cleaned_data['city'])
            district = get_object_or_404(Region, id=form.cleaned_data['district'])

            userAddress = UserAddress.objects.create(user=request.user,
                                                     receiver_name=receiver_name,
                                                     receiver_phone=receiver_phone,
                                                     province=province,
                                                     city=city,
                                                     district=district,
                                                     detailed_address=detailed_address,
                                                     is_default=is_default)
            return JsonResponse({'code':200,'message':'地址添加成功','data':{'userAddress_id':userAddress.id}})
        else:
            print(form.errors)
            return JsonResponse({'code':400,'message':'地址添加失败'})



# 三级联动的AJAX视图
@login_required
def get_cities(request, province_id):
    cities = Region.objects.filter(parent_id=province_id, level=2)
    data = [{'id': city.id, 'name': city.name} for city in cities]
    return JsonResponse(data, safe=False)

@login_required
def get_districts(request, city_id):
    districts = Region.objects.filter(parent_id=city_id, level=3)
    data = [{'id': district.id, 'name': district.name} for district in districts]
    return JsonResponse(data, safe=False)


@login_required
def address_update(request, pk):
    address = get_object_or_404(UserAddress, pk=pk, user=request.user)

    if request.method == 'POST':
        form = UserAddressForm(request.POST, instance=address)
        if form.is_valid():
            # 直接保存字符串形式的地区名称
            updated_address = form.save(commit=False)

            # 如果设置为默认地址，取消其他默认地址
            if updated_address.is_default:
                UserAddress.objects.filter(user=request.user, is_default=True).exclude(pk=pk).update(is_default=False)

            updated_address.save()
            messages.success(request, '收货地址更新成功！')
            return redirect('accounts:address_list')
    else:
        form = UserAddressForm(instance=address)

    provinces = Region.objects.filter(level=1)
    return render(request, 'address_form.html', {
        'form': form,
        'provinces': provinces,
        'address': address
    })


@login_required
def set_default_address(request, pk):
    address = get_object_or_404(UserAddress, pk=pk, user=request.user)

    # 取消当前所有默认地址
    UserAddress.objects.filter(user=request.user, is_default=True).update(is_default=False)

    # 设置新的默认地址
    address.is_default = True
    address.save()

    messages.success(request, '默认地址设置成功！')
    return redirect('accounts:address_list')


@login_required
def address_delete(request, pk):
    address = get_object_or_404(UserAddress, pk=pk, user=request.user)

    if address.is_default:
        messages.error(request, '不能删除默认地址，请先设置其他地址为默认')
    else:
        address.delete()
        messages.success(request, '收货地址已删除')

    return redirect('accounts:address_list')


