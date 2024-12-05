from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .models import *

import logging
# Создание базового логирования
logging.basicConfig(filename='errors.log', level=logging.INFO)

# Create your views here.
# отображение базы данных на отдельной странице
def database(request):
    logging.info('Джанго. Просмотр базы данных')
    # подключение моделей из базы данных и сохранение
    spacestore = Spacestore.objects.all()

    context = {
        'spacestore':spacestore
    }

    return render(request, 'spacestore/database.html', context)


# функции для отображения главной страницы
def primary(request):
    logging.info('Джанго. Просмотр главной страницы')
    return render(request, 'spacestore/primary.html')

# функции для отображения магазина и пагинатора
def store(request):
    logging.info('Джанго. Пользователь смотрит страницу магазина')
    # Получаем количество элементов на странице, по умолчанию 2
    items_per_page = int(request.GET.get('items_per_page', 2))
    # достается список игр
    spaceproducts = Spacestore.objects.all().order_by('id')
    # что размещается на страницах и в каком количестве
    paginator = Paginator(spaceproducts, items_per_page)
    # для перемещения
    page_number = request.GET.get('page')
    # страница как объект, передался номер страницы
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj, 
        'request': request
    }
    return render(request, 'spacestore/spacestore.html', context)


# функции для покупки товара
def buy_product(request, product_id):
    product = get_object_or_404(Spacestore, id=product_id)
    
    if 'cart' not in request.session:
        request.session['cart'] = []
    request.session['cart'].append(product.id)
    request.session.modified = True
    logging.info('Джанго. Корзина создана')
    return redirect('spacestore:cart')  # Перенаправление на страницу корзины


def cart(request):
    cart = request.session.get('cart', [])
    products = Spacestore.objects.filter(id__in=cart)
    total_cost = sum(product.cost for product in products)
    logging.info('Джанго. Корзина заполнена')
    return render(request, 'spacestore/cart.html', {'products': products, 'total_cost': total_cost})


def clear_cart(request):
    if request.method == 'POST':
        # Очищаем корзину
        request.session['cart'] = []
        logging.info('Джанго. Корзина очищена')
    return redirect('spacestore:cart')  # Перенаправляем обратно в корзину


