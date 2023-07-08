

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .forms import TitleForms

from .filters import PostFilter # импортируем класс(будет выводить список объектов из БД) DetailView- отвечает за детали(за 1 продукт)
from .models import *
from datetime import datetime


class ProductsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'flatpages/news.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-id') # выводит список с конца не обяз по id делать
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['all_posts'] = Post.objects.all()
        context['all_posts'] = Post.objects.order_by('-dataCreation') # переворачивает список
        return context

class ProductsListMain(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'flatpages/index.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  
        return context

class NewsCategory(ListView):
    model = Post 
    template_name = 'flatpages/category_news.html' 
    context_object_name = 'news_category'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_sort'] = Post.objects.all().filter(postCategory=self.kwargs['pk'])
        #context['category_sort']= Post.objects.filter(postCategory=self.kwargs['pk'])
        # возьмет все посты отфильтрует по пост категории= по рк ( а в url адресе у нас тоже заложен рк) 
        return context




class ProductDetail(DetailView):
    model = Post
    template_name = 'flatpages/one_news.html' 
    context_object_name = 'one_news'

def news(request):
    return render(request, 'flatpages/news.html', {'title':'все новости'}) 

def search(request):
    return render(request, 'flatpages/search.html', {'title':'поиск новостей'}) 
   
class SearchList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'flatpages/search.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'search'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-time_create']
    queryset = Post.objects.order_by('-id')
    #paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  
        return context

    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        context ['title'] = TitleForms(self.request.GET or None )
        context ['filterset'] = self.filterset
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset =PostFilter(self.request.GET, queryset)
        return self.filterset.qs

def pageNotFound(request, exception):
   return HttpResponseNotFound('<h1>Страница не найдена</h1>')

# в этих функциях не уверена в правильности аргументов тут написала общий принцип исключений
def pageNotFound_500(request):
    return HttpResponseNotFound('<h1>Ошибка сервера</h1>')

def pageNotFound_403(request, exception):
    return HttpResponseNotFound('<h1>доступ запрещен</h1>')

#def pageNotFound_400(request, exception):
 #   return HttpResponseNotFound('<h1>невозможно обработать запрос</h1>')