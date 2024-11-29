from django.db import models
from sign_in.models import CustomUser

# Create your models here.
class Spacestore(models.Model):
    title = models.CharField(max_length=30)
    size = models.IntegerField()
    description = models.TextField()
    cost = models.DecimalField(decimal_places=2 , max_digits=15)
    photo = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    buyer = models.ManyToManyField(CustomUser, related_name='spacethings', blank=True)

    def __str__(self):
        return self.title
    

