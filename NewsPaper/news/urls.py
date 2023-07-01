from django.urls import path
from .views import *

urlpatterns = [

    
    path('', ProductsListMain.as_view(), name = 'home' ),
    path('index', ProductsListMain.as_view(), name = 'home'),
   
    path('one_news/', news, name='one_news'),
    path('news/', ProductsList.as_view(), name = 'news_page' ),
    path('one_news/<int:pk>', ProductDetail.as_view()),
]