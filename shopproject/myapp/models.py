from django.db import models

# Create your models here.
class Customer(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    father=models.CharField(max_length=100)
    email=models.EmailField()
    pass1=models.CharField(max_length=20)
    Phone=models.CharField(max_length=10)
    address=models.CharField(max_length=200)
    img2=models.FileField(upload_to='uploads/customer/')
    def __str__(self):
        return self.fname # int value not return but srt value returnable
    
class Category(models.Model):
    name=models.CharField(max_length=50)
    des=models.CharField(max_length=100)
    img1=models.FileField(upload_to='uploads/categary/')       
    def __str__(self):
        return self.name
class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.FloatField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    des=models.CharField(max_length=100)
    image=models.FileField(upload_to='uploads/products/')  
    def __str__(self):
        return self.name    

class cart(models.Model):
    cust_id=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    pro_id=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField(default=1)
