from django.urls import path, re_path
from .views import *

urlpatterns = [

    
    path('', ProductsListMain.as_view(), name = 'home' ),
    re_path(r'^index/', ProductsListMain.as_view(), name = 'home'),
    re_path(r'^news/', ProductsList.as_view(), name = 'news_page' ),
    path('one_news/', news, name='one_news'),
    path('one_news/<int:pk>', ProductDetail.as_view(), name = 'o_news'),
    path('search', SearchList.as_view(), name = 'search' ),
   
    #path('category_news/<slug:category_name>/', NewsCategory.as_view(), name = 'category') тоже работает в строке дает назв категории
    path('category_news/<int:pk>', NewsCategory.as_view(), name = 'category'),
    
]
