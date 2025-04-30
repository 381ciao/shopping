from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class CaptchaModel(models.Model):
    email = models.EmailField(unique=True)
    captcha = models.CharField(max_length=4)
    create_time = models.DateTimeField(auto_now_add=True)

class UserAddress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name='用户'
    )
    receiver_name = models.CharField(max_length=50, verbose_name='收货人')
    receiver_phone = models.CharField(
        max_length=11,
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '请输入正确的手机号码')],
        verbose_name='联系电话'
    )
    province = models.CharField(max_length=50, verbose_name='省')
    city = models.CharField(max_length=50, verbose_name='市')
    district = models.CharField(max_length=50, verbose_name='区/县')
    detailed_address = models.CharField(max_length=200, verbose_name='详细地址')
    is_default = models.IntegerField(verbose_name='默认地址',unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户收货地址'
        verbose_name_plural = '用户收货地址'
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.province}{self.city}{self.district}{self.detailed_address}"

# models.py
class Region(models.Model):
    LEVEL_CHOICES = (
        (1, '省'),
        (2, '市'),
        (3, '区/县'),
    )
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    level = models.IntegerField(choices=LEVEL_CHOICES)

    def __str__(self):
        return self.name
