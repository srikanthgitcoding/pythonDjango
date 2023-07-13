from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count, Min, Max, Avg, Value, F, Func
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView,RetrieveAPIView, RetrieveDestroyAPIView
from rest_framework import status
from .models import Product, Collection, Review, Cart, CartItem # here we added period(.) in front of models whic indicates it is in current folder
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from django_filters.rest_framework import DjangoFilterBackend # this give us genric filktering
from .filters import ProductFilter
from django.db.models.functions import Concat

# Create your views here.
#======================= (1) =================================
    # CREATE VIEW USING DJANGO HTTP REQUEST AND RESPONSE   (1)

# def product_list(request):
#     return HttpResponse("ok")

#============================== (2) ==================================================

        #CREATE VIEWS USING REST FRAMWORK RESPONSE  AND DECORATORS (2)

@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'GET':
        query_set = Product.objects.all()[0:5]
        serializer = ProductSerializer(query_set, many=True) # many to true so that serializer knows to itertae  over query set n convert each product obj to dict
        return Response(serializer.data) # the view u get is differnet which is browsable api
    elif request.method == 'POST':
        print("*********", request.data)
        serializer = ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)#201 object created


@api_view(['GET','PUT',"DELETE"])# when u add post here in browser u can see text box
def product_detail(request, id):
    # try:
    #    product = Product.objects.get(pk=id) # it return product object
    #    print("product", product)
    #    serializer = ProductSerializer(product) #it convert product object to  dictionary
    #    return Response(serializer.data) # get the dictionary form ser.data
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)# this is one way but there is better way to this   
    product = get_object_or_404(Product, pk=id) # it return product object
    if request.method == 'GET':
        print("product", product)
        serializer = ProductSerializer(product) #it convert product object to  dictionary
        return Response(serializer.data) # get the dictionary form ser.data
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response({"error" : "product can not be dlete since it is associated with order item"})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    

#============================== (3) ==================================================
                    #3 class based views


# class ProductList(APIView):
#     def get(self,request):
#        qs = Product.objects.all()[0:5]
#        serializer = ProductSerializer(qs, many=True, context={'request':request})
#        return Response(serializer.data, status=status.HTTP_200_OK)
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)  
# 

# class ProductDetails(APIView):
#     def get(self,request, id):
#         singleproduct = get_object_or_404(Product, pk=id)
#         print("prodyct****", singleproduct)
#         serializer = ProductSerializer(singleproduct)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self,request, id):
#         prod = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(prod, data= request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#============================== (4) ==================================================

# BY IMPORTING mixins(GENERIC VIEWS) FROM RESTFRAMEWORK VIEWS

class ProductList(ListCreateAPIView):

    ''' list create api view handle fteching the list and create new record'''

    # the below 2 methods are use ful if u have logic 
    # in generic api vew class - 
    #queryset = Product.objects.all()[0:5]
    serializer_class = ProductSerializer
    def get_queryset(self):
        return Product.objects.filter({"title":"Civil Engineer"}).count()

    # below 2 mthods r useful when u have some specila logic or conditions else u can use quesry set and serializer class attributes
    # def get_queryset(self): # here we are overriding get query set
    #     return Product.objects.all()[0:5]
    # def get_serializer_class(self):
    #     return ProductSerializer 
    def get_serializer_context(self): # here we dont have special attribute to specify serializer context that is why we use or override  get seri context method 
        return {'request':self.request} #to get request object use - self.request

class ProductDetails(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self,request,pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({"error" : "product can not be dlete since it is associated with order item"})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   


#============================== (5 view sets) ==================================================
# if u see the generic view we have repeated code in muliple methods like#
# query set amd serializer 
class ProductViewSet(ModelViewSet):
    #queryset = Product.objects.all() #viewset
    def get_queryset(self):
        #print("count", Product.objects.filter("title").count())
        # print("agrregating objects", Product.objects.aggregate(Count("title"))) #agrregating objects {'title__count': 100}
        # print("agrregating objects", Product.objects.aggregate(Count("slug"))) #agrregating objects {'slug__count': 100}
        # print("agrregating objects", Product.objects.aggregate(slugName = Count("slug"))) #agrregating objects {'slugName': 100}
        # print("agrregating unit price min", Product.objects.aggregate(unit_price = Min("unit_price"))) #get minium unit price
        # print("agrregating unit price max", Product.objects.aggregate(unit_price = Max("unit_price"))) #get minium unit price
        # #combine both
        # print("agrregating unit price max", Product.objects.aggregate(count= Count("title"), unit_price = Max("unit_price"))) #Joins and aggregates¶
        # #get minium unit price
        # annotae objects 
        print("annotaet**************",Product.objects.annotate(is_new=Value(True)))
        print("annotaet**************",Product.objects.annotate(new_id=F('id')))
        print("Func Object**************",Product.objects.annotate(titleDes=Func(F('title'),Value(''),F('description'),function='CONCAT')))
        print("###", Product.objects.select_related("collection").all().order_by("id").annotate(titleDes=Func(F('title'),Value(''),F('description'),function='CONCAT')))
        qs = Product.objects.select_related("collection").all().order_by("id")
        
        return qs
    
    serializer_class = ProductSerializer
    print("serializeclass###############", serializer_class)
    # def get_queryset(self):
    #     print("##log self.request - ", self.request) #self.request
    #     print("##log query params - ", self.request.query_params) #<QueryDict: {'collection_id': ['3']}>
    #     qs = Product.objects.all()
    #     collection_id = self.request.query_params.get("collection_id") #quey params
    #     print("##log collection_id is 3", collection_id) #<QueryDict: {'collection_id': ['3']}>

    #     if collection_id is not None:
    #         qs = qs.filter(collection_id = collection_id)        
    #     return qs
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]# this adds filter button to UI along with this u should add some fields , filter_backends,filterseta_fields both are predefined attributes if u mispell it will not work
    filterset_fields = ['collection_id'] # here what if I want unit_price to be filter say = 10 it works but > or < some value it doesnt work so we have to create custom fikltering
    filterset_class = ProductFilter
    search_fields = ['title',"description"] # this adds search box in UI
    ordering_fields = ['unit_price','last_update'] #search bar contains this - ordering=-last_update # sorting ascending or descing order
    # usually searching u get -  collection_id = 1 however while sorting it becomes - ordering= unit_price or -unit_price
    # def get_queryset(self):  #filteringbackedns
    #     qs = Product.objects.all()
    #     unitprice= self.request.query_params.get("unit_price")
    #     print("unit price", unitprice)
    #     if unitprice is not None:
    #         qs = qs.filter(unit_price = unitprice)
    #     return qs    
    
    
    def destroy(self,request,id):
        product = get_object_or_404(Product, id)
        if product.orderitems.count() > 0:
            return Response({"error" : "product can not be dlete since it is associated with order item"})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   

 #allow - tells us what http methods are supported at this end point 
 #options - which we can used to see what operations or what methods available
 #when u print self.request -u get this - <rest_framework.request.Request: GET '/store/products/?collection_id=3'> for the url http://localhost:8000/store/products/?collection_id=3
#when u print self.request -u get this - <rest_framework.request.Request: GET '/store/products/> for the url http://localhost:8000/store/products/
##quey params(basically start with question mark followed by key value ?collection_id= 2) - self.request.query_params.get("collection _id")) - what if we dont have collection _id we get an error that is why we added .get method it rertusn none if collectiion is diesnt exist 
# or self.request.query_params["collection _id"])
#filteringbackedns - when we iuse filtering backends we dont need to overide get_queyset method

#================================ collection object ================================================

@api_view(["GET"])
def collection_list(request):
    if request.method == "GET":
        queryset = Collection.objects.all()[:5]
        serializer = CollectionSerializer(queryset, many=True)        
        return Response(serializer.data)
        

@api_view(['GET','DELETE']) # this decorator accepts arry of strings that specifies http methods get supports by default
def collection_detail(request,id):
    collection = get_object_or_404(Collection,pk=id)
    if request.method == 'GET':
        collectionSerialzer1 = CollectionSerializer(collection)
        return Response(collectionSerialzer1.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if Product.objects.count() > 0:
            return Response({"error":"collection is associated with product so cant be deleted"})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    


#collection view in using generic views 

class CollectionClass(ListCreateAPIView):
    queryset = Collection.objects.all().order_by("id")
    serializer_class = CollectionSerializer

    # def get_queryset(self):
    #     return Collection.objects.all().order_by("id")

    # def get_serializer_class(self):
    #     return CollectionSerializer

class CollectionDetailClass(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    
    # def get_queryset(self, request, id):
    #     return Collection.objects.get(pk=id)

    # def get_serializer_class(self):
    #     return CollectionSerializer  

    def destroy(self, request, pk, **kwargs):
        if Product.objects.count() > 0:
            return Response({"error":"collection is associated with product so cant be deleted"})  

##========================= REVIEWS VIEW =======================================================


class ReviewsViewSet(ModelViewSet):
    queryset =  Review.objects.all()
    serializer_class = ReviewSerializer

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


##========================= Cart VIEW =======================================================

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer


    # def get_queryset(self):
    #     query_set = Cart.objects.select_related("product").all()
    #     print("queryset", query_set)
    #     return query_set

class CartItemsViewSet(ModelViewSet):
    #how to allow only few http mehotds on this method
    http_method_names = ['get','post','patch','delete'] # all these methods has to be in lower case
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method  == 'PATCH':
            return UpdateCartItemSerializer    
        return CartItemSerializer        
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['lookupcart_pk']}    

    # serializer_class = CartItemSerializer
    def get_queryset(self):
        print("seld#####", self.kwargs['lookupcart_pk'])
        return CartItem.objects.filter(cart_id=self.kwargs['lookupcart_pk']). \
            select_related("product")