from django.db import models
from django.db.models.query_utils import select_related_descend
import datetime as d
# Create your models here.
class Item(models.Model):
    name = models.CharField(unique=True,max_length=30)
    barcode = models.PositiveIntegerField(unique=True)
    wholesale_pricse = models.PositiveIntegerField()
    retailer_pricse = models.PositiveIntegerField()
    stock = models.IntegerField()
    description = models.TextField()
    class Meta:
         ordering = ['name']
    def __str__(self):
        return self.name;
        
class Khaata(models.Model):
    name = models.CharField(max_length=100,unique=True)
    credit = models.IntegerField(default=0)
    credit_limit= models.IntegerField()
    credit_warning= models.PositiveIntegerField()
    cnic = models.PositiveIntegerField(blank=True,null=True)
    contact = models.PositiveIntegerField()
    email = models.EmailField(blank=True,null=True)
    created_at = models.DateField()
    updated = models.DateTimeField(auto_now_add=True)
    class Meta:
         ordering = ['name']
    def __str__(self):
        return self.name    
class Bill(models.Model):
    customer_name = models.CharField(max_length=100)
    amount = models.FloatField()
    profit = models.FloatField(default=0)
    khaata_name = models.ForeignKey(Khaata,on_delete=models.CASCADE)
    buyername = models.CharField(max_length=50)
    genrated_date = models.DateTimeField(default=d.datetime.now())
    details = models.TextField()
    class Meta:
         ordering = ['-genrated_date']
    def __str__(self):
        return self.customer_name + str(self.id)
    


    
    