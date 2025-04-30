from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
User = get_user_model()

from django.urls import reverse
# Create your models here.
class Category(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='分类名称'  # 添加中文名称
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='分类URL标识'  # 添加中文名称
    )

    class Meta:
        ordering = ('name',)
        verbose_name = '商品分类'  # 单数形式显示名称
        verbose_name_plural = '商品分类'  # 复数形式显示名称

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name='所属分类'  # 添加中文名称
    )
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='商品名称'  # 添加中文名称
    )
    slug = models.SlugField(
        max_length=200,
        db_index=True,
        verbose_name='商品URL标识'  # 添加中文名称
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True,
        verbose_name='商品图片'  # 添加中文名称
    )
    description = RichTextField(
        blank=True,
        verbose_name='商品描述'  # 添加中文名称
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='商品价格'  # 添加中文名称
    )
    available = models.BooleanField(
        default=True,
        verbose_name='是否上架'  # 添加中文名称
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'  # 添加中文名称
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'  # 添加中文名称
    )

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]
        verbose_name = '商品'  # 单数形式显示名称
        verbose_name_plural = '商品'  # 复数形式显示名称

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id, self.slug])

    def __str__(self):
        return self.name

class ProductComment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    pub_time = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments',verbose_name='所属博客')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='用户')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-pub_time']