from django.db import models
from django.contrib.auth.models import User

# User -built-in model used

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.FloatField()
    details=models.TextField(blank=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)


