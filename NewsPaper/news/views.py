
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import ListView, DetailView # импортируем класс(будет выводить список объектов из БД) DetailView- отвечает за детали(за 1 продукт)
from .models import Post

class ProductsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'flatpages/news.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-id') # выводит список с конца
    
class ProductsListMain(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'flatpages/index.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-id')

class ProductDetail(DetailView):
    model = Post
    template_name = 'flatpages/one_news.html' 
    context_object_name = 'one_news'

def news(request):
    return render(request, 'flatpages/news.html', {'title':'все новости'}) 
   

# Create your views here.

def pageNotFound(request, exception):
   return HttpResponseNotFound('<h1>Страница не найдена</h1>')

# в этих функциях не уверена в правильности аргументов тут написала общий принцип исключений
def pageNotFound_500(request):
    return HttpResponseNotFound('<h1>Ошибка сервера</h1>')

def pageNotFound_403(request, exception):
    return HttpResponseNotFound('<h1>доступ запрещен</h1>')

#def pageNotFound_400(request, exception):
 #   return HttpResponseNotFound('<h1>невозможно обработать запрос</h1>')