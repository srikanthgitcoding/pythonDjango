from django.db import models
import uuid
from django.conf import settings #cup2

# Create your models here.
class Promotion(models.Model):
    description = models.CharField(max_length=255) 
    discount = models.FloatField() 
    #product_set - that return all the prodcust that applied to

class Collection(models.Model):
    title = models.CharField(max_length=255)
    #products = models.ForeignKey(Product) 
    featured_product = models.ForeignKey("Product", on_delete = models.SET_NULL, null = True, related_name="test")#14

    def __str__(self) -> str:  
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug =  models.SlugField()#slug 
    description = models.TextField(null=True,blank=True)
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection,on_delete=models.PROTECT,null=True)#12
    promotions = models.ManyToManyField(Promotion)#p

    # def __str__(self) -> str:
    #     return self.title

class Cart(models.Model):
   #overriding default generated primary key 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        
    )
    #we have add unique constatnrt when a client increase s quanity it shoulnt create newcart item 
    # we should always make sure there is only single instance of cart and product
    class Meta:
        unique_together = [['cart','product']]

class Customer(models.Model):
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_GOLD = "G"

    MEMBERSHIP_CHOICES= [
        (MEMBERSHIP_BRONZE, "Bronze"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_GOLD, "Gold"),
    ] #7 
    # first_name = models.CharField(max_length=50)    
    # last_name = models.CharField(max_length=50)    
    # email = models.EmailField(unique=True) #5    
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True) #6
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE) #cup1 when u delete user associated customer record gets deleted 
    
    def __str__(self): #cup3
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta: #cup4
        ordering =  ['user__first_name','user__last_name']   

    # class Meta:
    #     db_table = "store_customers"
    #     indexes = [
    #         models.Index(fields=['last_name', 'first_name']) #15
    #     ]

class Order(models.Model):
    #8
    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_COMPLETE = "C"
    PAYMENT_STATUS_FAILED= "F"

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_COMPLETE, "Complete"),
        (PAYMENT_STATUS_FAILED, "Failed"),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)#30
    product = models.ForeignKey(Product,on_delete=models.PROTECT, related_name="orderitems")
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)

#9
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    #customer = models.OneToOneField(Customer, on_delete = models.CASCADE,primary_key=True) #10
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE) #11
    zip = models.CharField(max_length=255,default="12345")


class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name="reviews")    
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True) #noew

#choice fileds
#every model by default has an id field 
#5 - unique true so that we dont end up with duplicate emails
#6 - nullable
#7 - ADDING THIS IN CAPITAL WHICH MEANS VALUES ARE NOT GNG TO BE CHANGED
#8 - this class is of type choice filed
#9 - one to one relation ship
#10 - what should happen when customer deleted 
## on_delete = models.CASCADE - when we delete customer the associated address also will be deleted this is the cascade behaviour
## on_delete = models.SET_NULL - if this filed accepts null values - ewhen the customer gets deleted this fileds will be set to null value
## on_delete= models.PROTECT - models.PROTECT - with this we can prevent the deletion if there is a child associated with this parent we cant delete that parent first we have to dlete the child
## which values we use it depends on the requirement 
## primary_key = true - primary kjey dont allow duplicate values
## if we dont set pk here jango will create asnother field called id and evert addees ius gonna hgave an id that means we gonna ebnd up one to many relationship
#11
## how to create one to many relationship ?
## a cutomer can have multiple addresses so we can change tge one to one relantion ship to one to many
#p
## with this implimentation jango is going to create reverse relations ship in the promotion class #product_set
  
#what is circular dependency?
## sometimes we can have multiple relationships bw products - above we have 2 relationships bw collections and products
## a circular dependecy happens when 2 classes depeds on each other at the same time 
## a product class is gonna depend on collectiom class and at rhe same time collection class is fonne dependent on product class
## 12 - here we have deoendecy from product class towards collection class 
#14
## product is not defined error- because product class cretaed after collection class - to solve this prob wrap 
## product in double quotes
## on_delete = models.SET_NULL, - make this fields nullable

#collection can have multiple products
# customer '' orders
# orders '' item 
# cart '' Item

#30 on_delete=models.PROTECT
## if we accidentally delete an order here we dont end up deleting order items so if an order has atleast one item we will not be able to delete it 
#slug - 
## in chrom if we search for a question in address bar u can see the id of the question and the actual queation it self  this is called slug 
## slug only contains letters number - _ if there is a space in question it gets replacs by -
## why to add slug - to make it easier for serach engines to find our content - this is search engoine optimisation technique
## when u give slug to our products search engine can easily find our product

#15 we use indeing to speed up our queries

#noew  when we create review object the fata auto populates
