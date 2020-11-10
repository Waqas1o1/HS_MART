from django.http import request
from django.shortcuts import render,HttpResponse
import json
from .models import Item,Khaata,Bill
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def index(request):
    return render(request,'Store_App/index.html')
def ItemScanner(request,code):
    products = Item.objects.all()
    send_pdt = []
    for p in products:
        if code == p.barcode:
            send_pdt.append({'Name':p.name,'Barcode':p.barcode,'Retailer_pricse':p.retailer_pricse,'Wholesale_pricse':p.wholesale_pricse,'Description':p.description})
            return HttpResponse(json.dumps(send_pdt,default=str))
    return HttpResponse('Not found');            
def autocompleteModel(request):
    if request.is_ajax():
        items = Item.objects.values('name')
        itemlist = []
        for i in items:
            itemlist.append(i['name'])
        print(itemlist)
        data = json.dumps(itemlist)
        return HttpResponse(data);

def AddItemBarcode(request,barcode):
    if request.is_ajax():
        print(barcode)
        products = Item.objects.filter(barcode__exact=barcode)
        if len(products) >0 :
            send_pdt = []
            # print(products)
            for p in products:
                send_pdt.append({'Name':p.name,'Barcode':p.barcode,'Retailer_pricse':p.retailer_pricse,'Wholesale_pricse':p.wholesale_pricse,'Description':p.description,'Stock':p.stock})
            return HttpResponse(json.dumps(send_pdt,default=str))
    return HttpResponse('Not found');            
def AddItemByPdtName(request,pdtname):
    if request.is_ajax():
        products = Item.objects.filter(name__exact=pdtname)
        if len(products) >0 :
            send_pdt = []
            for p in products:
                send_pdt.append({'Name':p.name,'Barcode':p.barcode,'Retailer_pricse':p.retailer_pricse,'Wholesale_pricse':p.wholesale_pricse,'Description':p.description,'Stock':p.stock})
            return HttpResponse(json.dumps(send_pdt,default=str))
    return HttpResponse('Not found');            

def autosuggest(request):
    product_name = request.GET.get('term')
    products = Item.objects.filter(name__icontains=product_name)
    send_pdt = []
    for p in products:
        send_pdt.append(p.name)
    return HttpResponse(json.dumps(send_pdt,default=str))

def Find_Khaata(request):
    khata_name = request.GET.get('term',None)
    if khata_name is not None:
        khaaty = Khaata.objects.filter(name__icontains=khata_name)
        send_pdt = []
        for p in khaaty:
            send_pdt.append(p.name)
        print(send_pdt)
        return HttpResponse(json.dumps(send_pdt,default=str))
def GenrateBill_Genrated(request):
    if request.is_ajax():
        cartlist = request.POST.get('CartLists')
        Khaata_Name = request.POST.get('khaata')
        total_amount = request.POST.get('total_amount')
        discount = request.POST.get('discount')
        try:
            cart = json.loads(cartlist)
            is_Khaata = Khaata.objects.get(name__exact=Khaata_Name)
            if is_Khaata.credit < is_Khaata.credit_limit:
                waring = '';
                if  is_Khaata.credit >= is_Khaata.credit_warning:
                    waring = '<p>&#128540;</p> <strong>Warning ! Passe De DO</strong>' 
                   #Deduct Item From Stock
                for i in cart:
                    if i  is not None:
                        itm = Item.objects.get(name__exact=i['Name'])
                        if itm.stock <= 0:
                            return HttpResponse(f'<p style="font-size:100px">&#128529;</p> <h3>Mukk Gye {i["Name"]} </h3>''')
                        rmg_stock = itm.stock - i['Quantity'] 
                        if  rmg_stock < 0:
                            print(f'{itm.stock} , {rmg_stock}')
                            return HttpResponse(f'<p style="font-size:100px">&#128556;</p> <h3>Stock me itni  {i["Name"]} nhi hain</h3>''')
                        itm.stock -=  i['Quantity']
                        itm.save()
                Bill_Genrated = Bill(customer_name=Khaata_Name,khaata_name=is_Khaata,amount=total_amount,details=cart[0])
                Bill_Genrated.save()
                # Add Credit
                is_Khaata.credit += int(total_amount)
                is_Khaata.save()
             
                genrate_bill = {"Alert":waring,
                                "Order_ID":Bill_Genrated.id,
                                'Khaata':is_Khaata,'CustomerName':is_Khaata.name,
                                'Bill':Bill_Genrated,
                                'CartList':cart,
                                'SubTotal':int(total_amount) + int(discount),
                                'Discount':discount,
                                'TotalPricse':total_amount
                                }
                bill_page = render(request,'Store_App/Bill.html',genrate_bill)
                return bill_page
            elif is_Khaata.credit >= is_Khaata.credit_limit:
                return HttpResponse('''<span style='font-size:100px;'>&#128545;</span>
                                        <h3 style='color:red'>Bill Bharo Uddar BAND...</h3>''') 
        except ObjectDoesNotExist:
                return HttpResponse('''<span style='font-size:100px;'>&#128530;</span>
                            <h3>Khaat Tu sahi Likho...</h3>''')
        except IndexError:
            return HttpResponse('''<span style='font-size:100px;'>&#128530;</span>
                            <h3>Empity List...</h3>''')

