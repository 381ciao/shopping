from django.shortcuts import render, get_object_or_404,redirect,reverse
from .models import Category, Product,ProductComment
from django.views.decorators.http import require_GET,require_POST
from django.db.models import Q
from django.contrib import messages

def index(request):
    products = Product.objects.filter(available=True).order_by('name')[:9]
    return render(request, 'index.html',context={'products':products})

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    print(category_slug)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'detail.html', {'product': product})

@require_GET
def product_search(request):
    query = request.GET.get('query')
    if query:
        products = Product.objects.filter(Q(name__icontains=query))
    return render(request, 'search_list.html',context={'products': products})

@require_POST
def product_comment(request):
    product_id = request.POST.get('product_id')
    content = request.POST.get('content')

    # 获取商品对象
    product = get_object_or_404(Product, id=product_id)

    # 创建评论
    ProductComment.objects.create(
        product=product,
        content=content,
        user=request.user
    )

    messages.success(request, '评论已提交！')

    # 使用正确的参数名重定向
    return redirect(reverse('products:product_detail', kwargs={
        'id': product.id,
        'slug': product.slug
    }))