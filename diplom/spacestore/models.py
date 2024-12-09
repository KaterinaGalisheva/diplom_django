from asgiref.sync import sync_to_async
from django.db import models
from sign_in.models import CustomUser

# Create your models here.
class Spacestore(models.Model):
    title = models.CharField(max_length=30)
    size = models.IntegerField()
    description = models.TextField(max_length=2000)
    cost = models.DecimalField(decimal_places=2 , max_digits=15)
    photo = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    buyer = models.ManyToManyField(CustomUser, related_name='spacethings', blank=True)

    def __str__(self):
        return self.title
    

# Асинхронная функция для получения данных из базы данных
@sync_to_async
def get_items_from_db():
    return list(Spacestore.objects.all())

# Асинхронная функция для получения описания товара из базы данных
@sync_to_async
def get_item_description_from_db(product_id):
    product = Spacestore.objects.get(id=product_id)
    return product.description

# Асинхронная функция для получения названия товара из базы данных
@sync_to_async
def get_item_title_from_db(product_id):
    product = Spacestore.objects.get(id=product_id)
    return product.title