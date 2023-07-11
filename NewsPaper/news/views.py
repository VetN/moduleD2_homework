

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .forms import *

from .filters import PostFilter # импортируем класс(будет выводить список объектов из БД) DetailView- отвечает за детали(за 1 продукт)
from .models import *
from datetime import datetime


class NewsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'flatpages/news.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-id') # выводит список с конца не обяз по id делать
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        #context['all_posts'] = Post.objects.all()
        context['all_posts'] = Post.objects.order_by('-dataCreation') # переворачивает список
        return context




class NewsListMain(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'flatpages/index.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'l_news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-id')
    ordering = ['-dataCreation']
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow() 
        context['news'] = Post.objects.order_by('-id') 
        return context




class NewsCategory(ListView):
    model = Post 
    template_name = 'flatpages/category_news.html' 
    context_object_name = 'news_category'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_sort'] = Post.objects.order_by('-id').filter(postCategory=self.kwargs['pk'])
        #context['category_sort']= Post.objects.filter(postCategory=self.kwargs['pk'])
        # возьмет все посты отфильтрует по пост категории= по рк ( а в url адресе у нас тоже заложен рк) 
        return context




class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/one_news.html' 
    context_object_name = 'one_news'

def news(request):
    return render(request, 'flatpages/news.html', {'title':'все новости'}) 

 



class SearchList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'flatpages/search.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'search'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-time_create']
    queryset = Post.objects.order_by('-id')
    paginate_by = 7
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        #context ['news_form'] = NewsForms(self.request.GET or None )
        #context ['filterset'] = self.filterset.qs
        return context

    #def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset =PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    
    
    

class AddList(ListView):
    model = Post 
    template_name = 'flatpages/add_news.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'add_news' 
    queryset = Post.objects.order_by('-id')
    paginate_by = 1
   
    form_class = AddNewsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow() 
        context['news'] = Post.objects.order_by('-dataCreation')
       
        context['form_my'] = AddNewsForm()
        return context
    # если делать руками
   # def post(self, request, *args, **kwargs):
        # берём значения для нового товара из POST-запроса отправленного на сервер
        title = request.POST['title']
        author_id = request.POST['author']
        content = request.POST['content']
        postCategory = request.POST['postCategory']
        #photo = request.POST['photo']
        post = Post(title=title, author_id =author_id, content=content) # создаём новый товар и сохраняем
        post.save()
        return super().get(request, *args, **kwargs) # отправляем пользователя обратно на GET-запрос.
    
    
    #если использовать стандартную форму post
    def post(self, request, *args, **kwargs):
        form_my = self.form_class(request.POST, request.FILES) # создаём новую форму, забиваем в неё данные из POST-запроса 
    
        if form_my.is_valid(): # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
            form_my.save()
 
        return super().get(request, *args, **kwargs)


def pageNotFound(request, exception):
   return HttpResponseNotFound('<h1>Страница не найдена</h1>')

# в этих функциях не уверена в правильности аргументов тут написала общий принцип исключений
def pageNotFound_500(request):
    return HttpResponseNotFound('<h1>Ошибка сервера</h1>')

def pageNotFound_403(request, exception):
    return HttpResponseNotFound('<h1>доступ запрещен</h1>')

#def pageNotFound_400(request, exception):
 #   return HttpResponseNotFound('<h1>невозможно обработать запрос</h1>')