from django.urls import path, include
from . import views # importing views from current folder
# from rest_framework.routers import SimpleRouter , DefaultRouter#(if we use this we get 2 additional features if u go to store u get varoius wnd points)
from rest_framework_nested import routers
from pprint import pprint #pretty printitng

router = routers.DefaultRouter() #default router
print("default router", router)

router.register("products", views.ProductViewSet, basename="Products") #parentr router 
router.register("carts", views.CartViewSet , basename="carts") #parentr router 

products_router = routers.NestedDefaultRouter(router,'products',lookup="product") # child router
products_router.register('reviews',views.ReviewsViewSet,basename='product-reviews') #basename

carts_router = routers.NestedDefaultRouter(router,'carts',lookup="lookupcart") #lookup filed acts as a pk in our view 
carts_router.register('items',views.CartItemsViewSet,basename='cart-items-basename') #basename


urlpatterns = router.urls + products_router.urls + carts_router.urls


#======================
#lookup if u want to fetch primary key from url use this it becomes - lookupcart_pk

# router = SimpleRouter() 
# router.register('products',views.ProductViewSet) # here forwaed slash is not required
#  # here forwaed slash is not required
# # router.register('collections',views.CollectionViewSet)

# domains_router = routers.NestedSimpleRouter(router, r'domains', lookup='domain')
# domains_router.register(r'nameservers', NameserverViewSet, basename='domain-nameservers')

# # pprint(router.urls)

# #way 1 to add urls pattermn
# # urlpatterns = router.urls

# # if u have any specific patterns 

# urlpatterns = [
#     path('',include(router.urls)),
#     #other paths gfoes here
# ]
#basename - base name is used to generate the name of our url patterns and by default janog rest framework uses the query set attribute(this one we set in the viewset function #viewset)
#to figure out the base name
#



# # urlpatterns = [ # urlpatterns is special variable and this is what jango looks for
# #     path('products/', views.product_list), # use path fn to create a url pattern object - here we r not calling sayhello() we r referncing it
# #     path('products/<int:id>/', views.product_detail),
# #     path('productsClass/', views.ProductList.as_view()), # this calss has a method called as_view()
# #     path('productsClass/<int:pk>', views.ProductDetails.as_view()), # this calss has a method called as_view()
# #     path('collections/', views.collection_list),
# #     path('collectionsClass/', views.CollectionClass.as_view()),
# #     path('collectionsClass/<int:pk>', views.CollectionDetailClass.as_view()),
# #     path('collections/<int:id>/', views.collection_detail)
# # ]

# #always end routes with froward slash
# #whenever we change code django server automatically restores itself

