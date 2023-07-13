from rest_framework import serializers 
from .models import Product, Collection, Review, Cart, CartItem
from decimal import Decimal

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', "product_count"]
    # pc = serializers.IntegerField(read_only=True)    
    product_count = serializers.SerializerMethodField(method_name="get_product_count")

    def get_product_count(self, collection : Collection):
        return collection.objects.count()

class ProductSerializer(serializers.ModelSerializer): #this class should inherit serializer class from serializers module 
    class Meta:
        model = Product
        fields = ["id", "title", "description","slug","unit_price","inventory", "price_with_tax", "collection_id"] #11
        collection = CollectionSerializer 
        #fields = "__all__"
        #serialize relationship jusing  PrimaryKeyRelatedField
        # collection = serializers.PrimaryKeyRelatedField(
        #     queryset = Collection.objects.all()
        # ) 

        #collection = serializers.StringRelatedField() 

    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product :Product):
        return product.unit_price * Decimal(1.1)
        
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","title","unit_price"]

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField() # the method u call should have get_followed byname of the filed ex- get_total_price
    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']

    def get_total_price(self,cart_item:CartItem): 
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    print("********serializer cart id", id)
    items = CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField()
    print("item", items)
    class Meta:
        model = Cart 
        fields = ['id','items', 'total_price']

    def get_total_price(self,cart:Cart):
        print("###", cart.items.all())
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','product', 'name','description','date']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self,value): # methos is validate_followed by field name
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("no products")
        return value

    def save(self, **kwargs):
        #fetch cart id 
        cart_id = self.context['cart_id']
        #read data athat user has posted
        
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id = cart_id, product_id = product_id) # this lines throws error if there is no cart item
            #update an existing item
            cart_item.quantity += quantity
            cart_item.save()
            self.instance =  cart_item # refer to model serializer save method create and update
        except CartItem.DoesNotExist:
            # create a new item
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data) 
        
        return self.instance    

    class Meta:
        model = CartItem
        fields = ['id','product_id', 'quantity'] 


    #here we are the same we reeated in model check code above
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6,decimal_places=2, source="unit_price") #1
    # price_with_tax = serializers.SerializerMethodField(method_name="calculte_tax")

    # def calculte_tax(self, product:Product):
    #     return product.unit_price * Decimal(1.1)


#1 how to change unit_price to price 
#11 dont use '__all__' fileds always add required fileds in fileds array 


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem 
        fields = ['quantity']

