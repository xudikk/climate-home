from datetime import timedelta

import requests
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings

# Create your views here.
from django.utils import timezone

from core.models import Product, Category, TgBot, Admin, Blog


def index(request, slug=None):
    products = Product.objects.all().order_by('-id')
    ctg = Category.objects.filter(slug=slug).first()
    if ctg:
        products = products.filter(ctg=ctg)

    ctx = {
        "products": products[:12],
        "newest": Product.objects.filter(date__gte=timezone.now() - timedelta(days=15)).order_by('-date'),
        "blogs": Blog.objects.all().order_by("-pk")[:3]

    }
    return render(request, 'index.html', ctx)


def detail(request, pk):
    prod = Product.objects.filter(id=pk).first()
    if not prod:
        raise Http404(
            "Bunday Maxsulot Topilmadi"
        )

    products = Product.objects.filter(ctg=prod.ctg).order_by('-pk')
    ctx = {
        "products": products,
        "prod": prod
    }

    success = request.session.get('success', None)
    ctx["success"] = success

    try: del request.session['success']
    except: ...

    return render(request, "detail.html", ctx)


def product(request, slug=None):
    ctg = Category.objects.filter(slug=slug).first()
    key = request.GET.get("search", '')
    if key or ctg:
        products = Product.objects.filter(Q(name__icontains=key) | Q(description__icontains=key))
    else:
        products = Product.objects.all().order_by('-id')

    if ctg:
        products = products.filter(ctg=ctg)

    ctx = {
        "ctg": ctg,
        "ctgs": Category.objects.all(),
        "products": products,
        'hots': products.filter(Q(discount__gt=1)).order_by('-discount')
    }
    return render(request, "products.html", ctx)


def send_message(request):
    if request.POST:
        data = request.POST
        product = Product.objects.filter(id=data.get("product_id", 0)).first()
        if not product:
            return redirect("home")
        message = f"Bizda Yangi Zakaz:\n" \
                  f"Xaridor: {data.get('user')}\n" \
                  f"Raqami: <b>{data.get('phone')}</b>\n" \
                  f"Maxsulot: {product.name}\n" \
                  f"Maxsulot saytda: {f'climatehome.uz/detail/{product.id}'}"
        product.order_count += 1
        product.save()
        token = TgBot.objects.first()
        for i in Admin.objects.all()[:3]:
            url = f'https://api.telegram.org/bot{token.bot_token}/sendMessage?chat_id={i.user_id}&text={message}&parse_mode=HTML'
            requests.get(url)
        request.session['success'] = "Zakaz Qabul Qilindi Adminlar tez orada siz bn aloqaga chiqishadi"
        return redirect("detail", pk=data['product_id'])

    return redirect("products")




