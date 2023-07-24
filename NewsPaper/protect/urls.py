from django.urls import path
from .views import IndexView

urlpatterns = [
    path('index_user/', IndexView.as_view(), name = 'personal'),
]