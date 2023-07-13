from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F #q is short for query
from store.models import Product
# Create your views here.
# view function takes a request and return response(http resp)
# it is a request handler
# 

def sayHello(request):
    query_set = Product.objects.only("title")
    print("query_set", query_set)
    return render(request,'hello.html',{"name":"srikanth", "result":list(query_set)}) # here we are returning html page to see this in browser view page sorce
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #Product.objects.select_related("collection").prefetch_related("promotions").all()

    #find producst invntory with < 10 and price < 20
    # qs = Product.objects.filter(inventory__lt = 10 , unit_price__lt = 20 ) #way 1
    # qs = Product.objects.filter(inventory__lt = 10).filter(unit_price__lt=20) #way 2 
    # #find producst invntory with < 10 or price < 20 - or operator
    # qs = Product.objects.filter(Q(inventory__lt = 10) | Q(unit_price__lt =20))
    # qs = Product.objects.filter(Q(inventory__lt = 10) | ~Q(unit_price__lt =20))# not operator
    # qs = Product.objects.filter(inventory = F('unit_price'))#in
    # #sorting
    # qs = Product.objects.order_by("title") #s1 ASC
    # qs = Product.objects.order_by("-title") #s1 DES
    # qs = Product.objects.order_by("-title").reverse() # noe the order is ASC
    # qs = Product.objects.order_by("unit_price","-title") #s2
    # qs = Product.objects.order_by("unit_price") #s3 returns query set
    # qs = Product.objects.order_by("unit_price")[0]  #s4 
    # qs = Product.objects.earliest("unit_price")  #s5  returns objects in ASC
    # qs = Product.objects.latest("unit_price")  #s5  returns objects in DES

    # #limiting results
    # qs = Product.objects.all()[0:5] # [0,1,2,3,4] return only first 5 
    # qs = Product.objects.all()[5:10] #[5,6,7,8,9]

    #Selecting fields to queries
    # id title desc firstname lastname - what if I want to read only id and title from table use - values()
    # qs = product.objects.values("id", "title").distinct() - distinct methos to remove duplicates and get unique ones
    # related fileds - using __ notation we can access related fileds
    # qs = product.objects.values("id", "title","collection__title")# here collection is atable and title is fileds of it
    # values() return bunch of dictionarys
    #values method will be used to for 
    #values_list - returns bunch of tuples 
    #Order_Item.objects.values('product_id').distinct()
    #get all the order item product ids and return those titles of the products
    # orderItemProductIds = Order_item.objects.values("product_id").distinct()
    # product.objects.values(id__in = orderItemProductIds).order_by("title")





    #try:
    # query_set_object = Product.objects.get(pk=0)#1
    # query_set_object = Product.objects.filter(unit_price=20)#10
    # query_set_object = Product.objects.filter(unit_price__gt = 20)
    # query_set_object = Product.objects.filter(unit_price__gte =20)
    # query_set_object = Product.objects.filter(unit_price__lt = 20)
    # query_set_object = Product.objects.filter(unit_price__lte = 20)
    #query_set = Product.objects.filter(unit_price__range = (20,30))
    #query_set = Product.objects.filter(title__contains = "cofee") # case sensitive if coffe is Cofee it will not work
    # query_set = Product.objects.filter(title__startswith = "coffee") 
    # query_set = Product.objects.filter(title__endswith = "coffee") 
    #query_set = Product.objects.filter(last_update__year = 2021) 
    #query_set = Product.objects.filter(description__isnull = True) 
    #query_set = Customer.objects.filter(email__contains = ".com") 
    #query_set = Collection.objects.filter(collection_featured_product__isNull = True)
    #query_set = Product.objects.filter(inventory__lt = 10)
    #query_set = Order.objects.filter(customer__id = 1)
    #query_set = Order.objects.filter(pk = 1)
    #  
    # print("--", query_set_object)
    # except ObjectDoesNotExist:
    #     pass    
    #3
    # for product in query_set_object:
    #     print("product",product)
    #for product in query_set_object (iterate over a query set) - at this moment django will executes querysetn get the resilts from db
    #list()
    #return HttpResponse("Hellow world")# return plain http rersponse # in browser right clxick view page soruce


#1 objects - this is a manager object - evry model in django has a attribute called objects this return a manager objects
#2 Product.objects.all()(this return a query set) - all is used to pullout all the data in the object
#filter () - get(0)
#3 query set is executed in mutiple scenarios 1) for loop 2) when convert to list( query_set_object) 3) access individual element query_set_object[0]
# at #1 django will not call db at this moment when u query set executes it gets called db 
#1 this query set has to be evaulvated to getthe objects
# for filed look ups like greter than less than search query sets and look for filed look ups
#10 get all the products whos unit price is = 20

#filed looks ups URL  - https://docs.djangoproject.com/en/4.1/ref/models/querysets/#field-lookups
#in(referncing fileds using F objects) - compare inventoy to unit price (u cant just add up - u have to use f objects in order to use it)
#s1 - order by - sort title using alphabates(default ASC) u can change the ordser by adding negative sign
#s2 unit price in asc title in desc
#s3 sort unit price and pick first one (up to this points we get a query set object )
#s4 but the moment we access individual element - the query set gets evaluvated  and then we get actual object
#Query set objects
#filter order_by reverse exclude 
#product = Product.objects.get(pk=id) - product Product object (12)


#supported query operators

# exact
# iexact
# contains
# icontains
# in
# gt
# gte
# lt
# lte
# startswith
# istartswith
# endswith
# iendswith
# range

# date
# year
# iso_year
# month
# day
# week
# week_day
# iso_week_day
# quarter
# time
# hour
# minute
# second

# isnull
# regex
# iregex

