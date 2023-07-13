from django.urls import path
from . import views # importing views from current folder

urlpatterns = [ # urlpatterns is special variable and this is what jango looks for
    path('hello/', views.sayHello), # use path fn to create a url pattern object - here we r not calling sayhello() we r referncing it

]

#always end routes with froward slash
#whenever we change code django server automatically restores itself