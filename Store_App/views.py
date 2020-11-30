from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
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
        products = Item.objects.filter(name__exact=pdtname.upper())
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

def Refund(request,id):
    try:
        if request.is_ajax():
            cartlist = request.POST.get('CartLists')
            total_amount = request.POST.get('refund_amount')
            bill = Bill.objects.get(id=id)
            refund_cartlist = json.loads(cartlist)
            old_cartlist = json.loads(bill.details)
            is_change = False
            print(old_cartlist) 
            # Find item from old_cart in refund_cart if exit then redetail bill
            # Refund Item --> Stock  
            # Refund Bill-->profit, amount, is_refunded_bill, details, is_refunded_bill,refunded_return  ,Khaate---> Credit 
            for refund in refund_cartlist:
                for old in old_cartlist:
                    if refund['Name'] == old['Name']:
                        if old['Quantity'] >= refund['Quantity']:
                            old['Quantity'] -= refund['Quantity']
                            if old['Quantity'] == 0:
                                i = Item.objects.get(name=old['Name'])
                                i.stock += refund['Quantity']
                                i.save()
                                bill.profit -=  i.retailer_pricse - i.wholesale_pricse
                                old_cartlist.remove(old)
                            else:
                                i = Item.objects.get(name=old['Name'])
                                i.stock += refund['Quantity']
                                i.save()
                                bill.profit -= i.retailer_pricse - i.wholesale_pricse
                                old['Total_pricse'] = old['Quantity'] * old['Pricse']
                            is_change = True
                        else:
                            return HttpResponse(
                                '''<span style='font-size:100px;'>&#128536;</span>
                                    <h3>Lalale ki jan jitni le hain us se zada retuen na kro...</h3></div>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" onclick="Close()">Close</button>
                                    </div>''')
            if is_change == False:
                return HttpResponse('''<span style='font-size:100px;'>&#128533;</span>
                                    <h3>Returning Nhi Ho sakti List Dubara Check Karin.
                                    <br/>
                                    Koi product Return Bill main mujood nhi...</h3></div>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" onclick="Close()">Close</button>
                                    </div>''')
            else:
                k = Khaata.objects.get(name=bill.khaata_name) 
                k.credit -= int(total_amount)
                if len(old_cartlist) <= 0:
                    k.save()
                    bill.delete()
                    return HttpResponse('''<span style='font-size:100px;'>&#128465;</span>
                                    <h3>Sab Wapaass....</h3></div>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" onclick="Close()">Close</button>
                                    </div>''')
                k.save()
                bill.amount -= int(total_amount)
                bill.is_refunded_bill = True
                bill.refunded_return = total_amount
                bill.details = json.dumps(old_cartlist)
                bill.save()

            print(old_cartlist)


        return HttpResponse('''<span style='font-size:100px;'>&#128530;</span>
                                <h3>Ho gya wapass Bro ab Jao...</h3></div>
                                </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" onclick="Close()">Close</button>
                                    </div>''')
    except ObjectDoesNotExist:
        return HttpResponse('''<span style='font-size:100px;'>&#129488;</span>
                                <h3>Asa Tu kuch Nazer me nhi aata...</h3></div>
                                </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" onclick="Close()">Close</button>
                                    </div>''')

def Find_Khaata(request):
    khata_name = request.GET.get('term',None).upper()
    if khata_name is not None:
        khaaty = Khaata.objects.filter(name__icontains=khata_name)
        send_pdt = []
        for p in khaaty:
            send_pdt.append(p.name)
        return HttpResponse(json.dumps(send_pdt,default=str))
def GenrateBill_Genrated(request):
    if request.is_ajax():
        cartlist = request.POST.get('CartLists')
        Khaata_Name = request.POST.get('khaata').upper()
        total_amount = request.POST.get('total_amount')
        discount = request.POST.get('discount')
        cash_deposit = request.POST.get('cash_deposit')
        try:
            if cash_deposit != '0':
                cash_return = int(cash_deposit) - int(total_amount) 
            else:
                cash_return = '0'; 
            cart = json.loads(cartlist)
            is_Khaata = Khaata.objects.get(name__exact=Khaata_Name)
            if is_Khaata.credit < is_Khaata.credit_limit:
                waring = '';
                if  is_Khaata.credit >= is_Khaata.credit_warning:
                    waring = '<p>&#128540;</p> <strong>Warning ! Passe De DO</strong>' 
                   #Deduct Item From Stock
                p = 0
                for i in cart:
                    if i  is not None:
                        itm = Item.objects.get(name__exact=i['Name'])
                        if itm.stock <= 0:
                            return HttpResponse(f'<p style="font-size:100px">&#128529;</p> <h3>Mukk Gye {i["Name"]} </h3>''')
                        rmg_stock = itm.stock - i['Quantity']
                        p += (itm.retailer_pricse - itm.wholesale_pricse) * i['Quantity'] 
                        if  rmg_stock < 0:
                            return HttpResponse(f'<p style="font-size:100px">&#128556;</p> <h3>Stock me itni  {i["Name"]} nhi hain</h3>''')
                        itm.stock -=  i['Quantity']
                        itm.save()
                Bill_Genrated = Bill(customer_name=Khaata_Name,khaata_name=is_Khaata,amount=total_amount,details=cartlist,genrated_date=datetime.now(),profit=p,cash_deposit=cash_deposit,cash_return=str(cash_return))
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
                                'TotalPricse':total_amount,
                                'cash_deposit':cash_deposit,
                                'cash_return':cash_return
                                }
                bill_page = render(request,'Store_App/Bill.html',genrate_bill)
                return bill_page
            elif is_Khaata.credit >= is_Khaata.credit_limit:
                return HttpResponse('''<span style='font-size:100px;'>&#128545;</span>
                                        <h3 style='color:red'>Bill Bharo Uddar BAND...</h3>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-primary" data-dismiss="modal">Continue</button>
                                            <button type="button" class="btn btn-secondary" onclick="Close()">Close</button>
                                        </div>''') 
        except ObjectDoesNotExist:
                return HttpResponse('''<span style='font-size:100px;'>&#128530;</span>
                            <h3>Khaat Tu sahi Likho...</h3></div>
                            </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-primary" data-dismiss="modal">Continue</button>
                                </div>''')
        except IndexError:
            return HttpResponse('''<span style='font-size:100px;'>&#128530;</span>
                            <h3>Empity List...</h3>
                            </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" onclick="Close()">Close</button>
                                </div>
                            ''')
        except ValueError:
            return HttpResponse('''<span style='font-size:100px;'>&#128545;</span>
                            <h3>Cash Likho Mazzak Na kro...</h3>
                            </div>
                                <div class="modal-footer">
                                   <button type="button" class="btn btn-primary" data-dismiss="modal">Sorry!</button>
                                </div>
                            ''')
