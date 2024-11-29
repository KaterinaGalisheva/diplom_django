from django.urls import path
from spacestore import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'spacestore'


urlpatterns = [
    path('', views.store, name='store'),
    path('database/', views.database, name='database'),
    path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
    path('cart/', views.cart, name='cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)