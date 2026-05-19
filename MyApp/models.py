from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    cid=models.AutoField(primary_key=True)
    cname=models.CharField(max_length=50)


    def __str__(self):
        return self.cname
    
class Product(models.Model):
    pid=models.AutoField(primary_key=True)
    pname=models.CharField(max_length=50)
    pprice=models.IntegerField()
    pdis=models.TextField()
    pimage=models.ImageField(upload_to='product')
    c_id=models.ForeignKey(Category, on_delete=models.CASCADE)


    def __str__(self):
        return self.pname

class Cart(models.Model):
    crt_id=models.AutoField(primary_key=True)
    p_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    u_id=models.ForeignKey(User, on_delete=models.CASCADE)
    quantity=models.IntegerField()

    def __str__(self):
        return self.u_id.username
    
    def sub_total(self):
        return self.p_id.pprice * self.quantity
    


class Wishlist(models.Model):
    w_id=models.AutoField(primary_key=True)
    p_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    u_id=models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.p_id.pname
    

class O_tracker(models.Model):
    otid=models.AutoField(primary_key=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status


class Order(models.Model):
    oid = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField()
    mobile = models.BigIntegerField()
    address = models.TextField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    amount = models.FloatField(default=0)
    zip = models.IntegerField()
    payment = models.CharField(max_length=20)
    order_status = models.ForeignKey(O_tracker, on_delete=models.CASCADE)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    odate = models.DateTimeField(auto_now_add=True)
    charges = models.IntegerField(default=0)

    def __str__(self):
        return self.u_id.username

class O_item(models.Model):
    O_item = models.AutoField(primary_key=True)
    o_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    p_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.IntegerField()

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']