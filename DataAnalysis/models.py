from django.db import models
from Store_App.models import Khaata
# Create your models here.
class Credit_Transsaction(models.Model):
    Transection = models.IntegerField()
    Transaction_Message = models.TextField() 
    Credit_Before_Transaction = models.IntegerField()
    Credit_After_Transaction = models.IntegerField()
    Khaata = models.ForeignKey(Khaata,on_delete=models.CASCADE)
    Transection_Date = models.DateTimeField(auto_now=True)
    Update = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.Khaata.name + 'On ' + self.Transection_Date + 'for ' + self.Transaction_Message