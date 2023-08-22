from django import views
from django.urls import path
from news.views import  subCategory, unsubCategory


#app_name = 'mail'
urlpatterns = [
    path('mail/subscribe/<int:pk>', subCategory, name = 'sub'),
    path('mail/unsubscribe/<int:pk>',unsubCategory, name = 'unsub'),
    

]