from django.db import models
from django.db.models import fields
import datetime
from Store_App.models import Khaata
# Create your models here.
class Transaction(models.Model):
    Transaction = models.IntegerField(default=0,blank=True)
    Transaction_Message = models.TextField(null=True,max_length=500) 
    Credit_Before_Transaction = models.IntegerField(null=True,blank=True)
    Credit_After_Transaction = models.IntegerField(null=True,blank=True)
    Khaata = models.ForeignKey(Khaata,on_delete=models.CASCADE)
    Transaction_Date = models.DateTimeField(auto_now=True)
    Update = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.Khaata.name + 'On ' + str(self.Transaction_Date) + 'for ' + self.Transaction_Message

    def save(self,*args,**kwargs):
        self.Credit_Before_Transaction = self.Khaata.credit
        self.Khaata.credit -= self.Transaction
        self.Khaata.save()
        self.Credit_After_Transaction = self.Khaata.credit
        super().save(*args, **kwargs)