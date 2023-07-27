"""
URL configuration for NewsPaper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static


from django.contrib import admin
from django.urls import include, path
from news.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('pages/', include('django.contrib.flatpages.urls')),
    path('',include('news.urls')),
    #path('news/',include('news.urls')),
    #path('one_news/', include('news.urls')),
    
    # пути для регистрации 
    path('sign/', include('sign.urls')),
    path('user/', include('protect.urls')),
    
    # прописываем путь при allauch
    path('accounts/', include('allauth.urls')),
    
    # путь к папке почтовых 
    path('mail/', include('mail.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = pageNotFound
handler500 = pageNotFound_500
handler403 = pageNotFound_403
#handler400 = pageNotFound_400