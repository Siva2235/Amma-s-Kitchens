from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Exclusive(models.Model):
    discount = models.CharField(max_length=20)
    rating = models.FloatField()
    img = models.ImageField(upload_to='pics')

class Choose(models.Model):
    img = models.ImageField(upload_to='pics')
    name = models.CharField(max_length=20)
    description = models.TextField()

class Special_categories(models.Model):
    img = models.ImageField(upload_to='pics')
    title = models.CharField(max_length=20)

class Special_Festivals(models.Model):
    img = models.ImageField(upload_to='pics')
    item_name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    badge = models.CharField(max_length=50, blank=True, null=True)

class Family_Packages(models.Model):
    img = models.ImageField(upload_to='pics')
    item_name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    badge = models.CharField(max_length=50, blank=True, null=True)

class Chef(models.Model):
    img = models.ImageField(upload_to='pics')
    item_name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    badge = models.CharField(max_length=50, blank=True, null=True)

class Refreshing_Drinks(models.Model):
    img = models.ImageField(upload_to='pics')
    item_name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    badge = models.CharField(max_length=50, blank=True, null=True)

class Quick_Bites(models.Model):
    img = models.ImageField(upload_to='pics')
    item_name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    badge = models.CharField(max_length=50, blank=True, null=True)



class Combo_Offers(models.Model):
    img = models.ImageField(upload_to='pics')
    item_name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    badge = models.CharField(max_length=50, blank=True, null=True)

class BreakFast(models.Model):
    name = models.CharField(max_length=100)
    data_category = models.CharField(max_length=40)
    price = models.IntegerField()
    image = models.ImageField(upload_to='pics')
    veg = models.BooleanField(default=True)

class Veg(models.Model):
    name = models.CharField(max_length=100)
    data_category = models.CharField(max_length=40)
    price = models.IntegerField()
    image = models.ImageField(upload_to='Veg')
    veg = models.BooleanField(default=True)    

class Non_Veg(models.Model):
    name = models.CharField(max_length=100)
    data_category = models.CharField(max_length=40)
    price = models.IntegerField()
    image = models.ImageField(upload_to='Non-Veg')
    veg = models.BooleanField(default=True)   

class Soups(models.Model):
    name = models.CharField(max_length=100)
    data_category = models.CharField(max_length=40)
    price = models.IntegerField()
    image = models.ImageField(upload_to='pics')
    veg = models.BooleanField(default=True)

class Pasta(models.Model):
    name = models.CharField(max_length=100)
    data_category = models.CharField(max_length=40)
    price = models.IntegerField()
    image = models.ImageField(upload_to='pics')
    veg = models.BooleanField(default=True)

class Snacks(models.Model):
    name = models.CharField(max_length=100)
    data_category = models.CharField(max_length=40)
    price = models.IntegerField()
    image = models.ImageField(upload_to='pics')
    veg = models.BooleanField(default=True)

class Starters(models.Model):
    name = models.CharField(max_length=100)
    data_category = models.CharField(max_length=40)
    price = models.IntegerField()
    image = models.ImageField(upload_to='pics')
    veg = models.BooleanField(default=True)    




class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    image = models.URLField(max_length=500, blank=True, null=True)
def __str__(self):
        return f"{self.quantity} x {self.name} ({self.user.username})"




class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField()
    phone_number = models.CharField(max_length=15)
    delivery_instructions = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')  # pending, confirmed, delivered, cancelled
    items = models.JSONField()  # Store cart items as JSON

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.order_date}"
    
    
class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20)  # card, upi, cod
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    
    # For card payments
    card_number = models.CharField(max_length=16, blank=True, null=True)
    card_expiry = models.CharField(max_length=5, blank=True, null=True)
    card_cvv = models.CharField(max_length=4, blank=True, null=True)
    
    # For UPI payments
    upi_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.payment_method}"