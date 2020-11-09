from django.db import models
from django.db.models.query_utils import select_related_descend

# Create your models here.
class Item(models.Model):
    name = models.CharField(unique=True,max_length=30)
    barcode = models.PositiveIntegerField(unique=True)
    wholesale_pricse = models.PositiveIntegerField()
    retailer_pricse = models.PositiveIntegerField()
    description = models.TextField()
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
    def __str__(self):
        return self.name    
class Bill(models.Model):
    customer_name = models.CharField(max_length=100)
    amount = models.FloatField()
    khaata_name = models.ForeignKey(Khaata,on_delete=models.CASCADE)
    buyername = models.CharField(max_length=50)
    genrated_date = models.DateTimeField(auto_now=True)
    details = models.TextField()
    def __str__(self):
        return self.customer_name + str(self.id)

