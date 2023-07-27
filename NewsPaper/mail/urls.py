from django.urls import path
from .views import  subCategory, unsubCategory


#app_name = 'mail'
urlpatterns = [
    path('mail/subscribe/<int:pk>', subCategory, name = 'sub'),
    path('mail/unsubscribe/<int:pk>',unsubCategory, name = 'unsub'),
]