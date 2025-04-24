from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Category(models.Model):
    """商品分类模型"""
    name = models.CharField('分类名称', max_length=100, unique=True)

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'
        ordering = ['name']

    def __str__(self):
        return self.name

class Goods(models.Model):
    name = models.CharField('商品名称', max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='商品分类'
    )
    sku = models.CharField('库存单位', max_length=50, unique=True)
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='卖家')
    is_active = models.BooleanField('是否上架', default=True)
    is_featured = models.BooleanField('是否推荐', default=False)
    is_bestseller = models.BooleanField('是否热销', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class GoodsImage(models.Model):
    # 商品图片
    Goods = models.ForeignKey(
        Goods,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='所属商品'
    )
    image = models.ImageField('图片', upload_to='goods/')
    is_featured = models.BooleanField('是否主图', default=False)

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = '商品图片'

    def __str__(self):
        return f"图片 {self.id} - {self.good.name}"
