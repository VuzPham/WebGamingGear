from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your models here.

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,null=True)
    def __str__(self):
        return str(self.name)
    
class Distributor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,null=True)
    description = models.TextField()
    price = models.IntegerField()
    rate = models.IntegerField()
    numbersell = models.IntegerField()
    image = models.ImageField(null=True, blank=False)
    Category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=False, related_name='products')
    def __str__(self):
        return f"{self.name} --- {self.Category} --- {self.price} --- {self.image} --- {self.rate} --- {self.numbersell}"

class Member(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    passWord = models.CharField(max_length=50,null=False)
    birth = models.DateField(default='2000-01-01',null=True)
    email = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.username

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(Member, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.name
    


class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    Customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    phoneNumber = models.CharField(max_length=11, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, default=1)
    Customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, blank=True, null=True)
    transaction_id = models.CharField(max_length=200, null=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('product', 'bill')

    def __str__(self):
        return f"Customer: {self.Customer.name} ---- Product: {self.product.name} ---- Bill: {self.bill.id} --- Quantity: {self.quantity}"


    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def get_cart_total(self):   
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

class Loai(models.Model):
    tenloai = models.TextField()

    def __str__(self):
        return self.tenloai

class OrderItem(models.Model):
    orders = models.ForeignKey('Orders', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Orders(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"

