

from django.http import HttpResponseNotFound
from django.shortcuts import redirect
#from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import *

from .filters import PostFilter
from .models import *
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin




class NewsList(ListView):
    model = Post 
    template_name = 'flatpages/news.html' 
    context_object_name = 'news' 
    queryset = Post.objects.order_by('-id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['all_posts'] = Post.objects.order_by('-dataCreation') 
        return context




class NewsListMain(ListView):
    model = Post  
    template_name = 'flatpages/index.html'  
    context_object_name = 'l_news' 
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
    context_object_name = 'news_category'
    
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_sort'] = Post.objects.order_by('-id').filter(postCategory=self.kwargs['pk'])
        return context




class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/one_news.html' 
    context_object_name = 'one_news'
    queryset = Post.objects.all()


 



class SearchList(ListView):
    model = Post  
    template_name = 'flatpages/search.html'  
    context_object_name = 'search' 
    ordering = ['-time_create']
    queryset = Post.objects.order_by('-id')
    paginate_by = 7
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        #context['choices'] = Post.CATEGORY_CHOICES если делать в фильтре 'exact'
        #context ['news_form'] = NewsForms(self.request.GET or None )
        #context ['filterset'] = self.filterset.qs
        return context

    #def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset =PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    


class NewsEditView(LoginRequiredMixin, ListView):
    template_name = 'flatpages/edit.html'
    context_object_name = 'news' 
    queryset = Post.objects.order_by('-id')
    #ordering = ['-dataCreation']
    paginate_by = 6
    form_class = AddNewsForm
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['news'] = Post.objects.order_by('-id') 
        
        #context['form_my'] = AddNewsForm()
        return context 



class AddNewsCreate(LoginRequiredMixin, CreateView):
    
    template_name = 'flatpages/add_news.html' 
    form_class = AddNewsForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    #если использовать стандартную форму post
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES) # создаём новую форму, забиваем в неё данные из POST-запроса 
    
        if form.is_valid():
            form.save()
            #obj = form_my.save()# чтобы записи не клонировались переход на другую страницу
            #return redirect('o_news', pk=obj.pk)
            return redirect('edit')
        else:
            return redirect('news_page') 
           #return super().get(request, *args, **kwargs) # отправляем пользователя обратно на GET-запрос.
    
    
    


class NewsUpdateView(UpdateView):
        #model = Post
        template_name = 'flatpages/add_news.html' 
        form_class = AddNewsForm
        success_url = '/edit/'
       
         # метод get_object мы используем вместо queryset, 
         # чтобы получить информацию об объекте который мы собираемся редактировать
        def get_object(self, **kwargs):
            id = self.kwargs.get('pk')
            return Post.objects.get(pk=id)
            
     


class NewsDeleteView(DeleteView):
    #model = Post
    template_name = 'flatpages/delete.html'
    queryset = Post.objects.all()
    success_url = '/edit/'




def pageNotFound(request, exception):
   return HttpResponseNotFound('<h1>Страница не найдена</h1>')

# в этих функциях не уверена в правильности аргументов тут написала общий принцип исключений
def pageNotFound_500(request):
    return HttpResponseNotFound('<h1>Ошибка сервера</h1>')

def pageNotFound_403(request, exception):
    return HttpResponseNotFound('<h1>доступ запрещен</h1>')

#def pageNotFound_400(request, exception):
 #   return HttpResponseNotFound('<h1>невозможно обработать запрос</h1>')

#def news(request):
   # return render(request, 'flatpages/news.html', {'title':'все новости'}) 
