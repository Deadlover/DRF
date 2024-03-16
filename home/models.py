from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator

def start_with_zeor(value):
    if value < 0:
        raise ValidationError(
            _("%(value)s cannot exist"),
            params={"value": value},
        )

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Fooditem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fooditems') 
    Name = models.CharField(max_length=50)
    descriptions = models.TextField(max_length=1000, null=True, blank=True)
    quantity = models.IntegerField(validators=[start_with_zeor])
    price = models.IntegerField()
    image = models.ImageField(upload_to="foodimage/")
    active = models.BooleanField(default=True)
    

    def __str__(self):
        return self.Name



class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.first_name}"
    
    @property
    def get_total(self):
        orderitems = self.items.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def get_all_total(self):
        orderitems = self.items.all()
        total = sum([item.quantity_item for item in orderitems])
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items') 
    food_item = models.ForeignKey(Fooditem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.food_item.Name}"
    
    @property
    def quantity_item(self):
        total = self.quantity * self.food_item.price
        return total
    
