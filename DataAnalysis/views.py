from typing import DefaultDict, Set
from Store_App.models import Bill
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from Store_App import models
from . import models as m
from Store_App import views as v
from datetime import datetime,timedelta
from django.db.models import Q
from django.core.paginator import Paginator
import json
# Create your views here.
def Bill_Analysis(request):
    if request.method == 'POST':
        if request.is_ajax():
            date_from = request.POST.get('date_from',None)
            date_to = request.POST.get('date_to',None)
            khaata = request.POST.get('khaata',None)
            bill = ''
            khaata = models.Khaata.objects.filter(name=khaata)
            if len(khaata) > 0 and date_from != '':
                d_f = datetime.strptime(date_from, '%m/%d/%Y') - timedelta(1)
                d_t = datetime.strptime(date_to, '%m/%d/%Y')
                d_t.strftime('%Y/%m/%d')
                bill = models.Bill.objects.filter(khaata_name=khaata[0]).filter(Q(genrated_date__date__gt=d_f) & Q(genrated_date__date__lte=d_t))
                print('Khaata and Date Filter')
            elif len(khaata) > 0 and date_from  == '':
                bill = models.Bill.objects.filter(khaata_name=khaata[0]).order_by('genrated_date__date')
                print('only khaata filter')
            elif len(khaata) == 0 and date_from != '' and date_to != '':
                d_f = datetime.strptime(date_from, '%m/%d/%Y') - timedelta(1)
                d_t = datetime.strptime(date_to, '%m/%d/%Y')
                d_t.strftime('%Y/%m/%d')
                print('only date filter')
                bill = models.Bill.objects.filter(Q(genrated_date__date__gt=d_f) & Q(genrated_date__date__lte=d_t))[:30]
            send_dict = []
            
            for b in reversed(bill):
                detail = json.loads(b.details)
                sub_total = 0
                for i in detail:
                    sub_total += i['Pricse']
                send_dict.append({"Name":b.customer_name,'Total_Amount':b.amount,'Khaata_name':str(b.khaata_name),'genrated_date':b.genrated_date,'details':detail,'SubTotal':sub_total})
            d = json.dumps(send_dict,default=str)
            return HttpResponse(d)
    bill = models.Bill.objects.all().order_by('genrated_date__date')[:50]
    send_list = []
    for b in reversed(bill):
        detail = json.loads(b.details)
        sub_total = 0
        for i in detail:
            sub_total += i['Pricse']
        send_list.append({"Name":b.customer_name,'Total_Amount':b.amount,'Khaata_name':b.khaata_name,'genrated_date':b.genrated_date,'details':detail,'SubTotal':sub_total})
    paginator = Paginator(send_list,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'DataAnalysis/Bill_Analysis.html',{'Bill':page_obj})

def Graph_Analysis(request):
    return render(request,'DataAnalysis/Profit_Analysis.html')
def Get_Graph(request,year):
    if request.is_ajax():
        print(year)
        bill = Bill.objects.filter(genrated_date__year=year).values('amount','profit','genrated_date')
        ls = []
        a = DefaultDict(int)
        p = DefaultDict(int)
        # date = l['genrated_date'].strftime('%d')
        for l in bill:
            month = l['genrated_date'].strftime('%b')
            a[month] += int(l['amount']) 
        
        for l in bill:
            month = l['genrated_date'].strftime('%b')
            p[month] += int(l['profit']) 
        
        ls.append(a)
        ls.append(p)

        return JsonResponse(ls,safe=False)

def Transaction(request):
    transactions = m.Transaction.objects.all().order_by('Transaction_Date')
    paginator = Paginator(transactions,30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'DataAnalysis/Transaction_Analysis.html',{'Transactions':page_obj})