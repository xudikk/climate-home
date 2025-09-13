from datetime import timedelta

import requests
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings

# Create your views here.
from django.utils import timezone

from core.models import Product, Category


def index(request, slug=None):
    ctg = None
    if slug:
        ctg = Category.objects.filter(slug=slug).first()
    if ctg:
        products = Product.objects.filter(ctg=ctg).order_by('-order_count')
    else:
        products = Product.objects.all().order_by('-order_count')[:12]

    ctx = {
        "products": products,
        "newest": Product.objects.filter(date__gte=timezone.now() - timedelta(days=7)).order_by('-date')

    }
    return render(request, 'index.html', ctx)


def detail(request, pk):
    prod = Product.objects.filter(id=pk).first()
    if not prod:
        raise Http404(
            "Bunday Maxsulot Topilmadi"
        )

    products = Product.objects.all().order_by('-order_count')
    ctx = {
        "products": products,
        "prod": prod
    }

    success = request.session.get('success', None)
    ctx["success"] = success

    try: del request.session['success']
    except: ...

    return render(request, "detail.html", ctx)


def send_message(request):
    print("aaaa")
    if request.POST:
        print("keldi")
        data = request.POST
        product = Product.objects.filter(id=data.get("product_id", 0)).first()
        if not product:
            print("bbbb")
            return redirect("home")
        message = f"Bizda Yangi Zakaz:\n" \
                  f"Xaridor: {data.get('user')}\n" \
                  f"Raqami: <b>{data.get('phone')}</b>\n" \
                  f"Maxsulot: {product.name}\n" \
                  f"Maxsulot saytda: {f'http://127.0.0.1:8000/detail/{product.id}'}"

        url = f'https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={settings.USER_ID}&text={message}&parse_mode=HTML'
        requests.get(url)
        request.session['success'] = "Zakaz Qabul Qilindi Adminlar tez orada siz bn aloqaga chiqishadi"
        return redirect("detail", pk=data['product_id'])

    print("bu yerda")
    return redirect("home")



