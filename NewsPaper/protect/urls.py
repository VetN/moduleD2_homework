from django.urls import path
from .views import IndexView, upgrade_me, upauthors

app_name = 'protect'
urlpatterns = [
    path('index_user/', IndexView.as_view(), name='personal'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('upauthors/', upauthors, name = 'upauthors')
]