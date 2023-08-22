from django.forms import ValidationError
from requests import delete
from .models import *
from .forms import *
from .filters import PostFilter

from django.db.models.query import QuerySet
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
#from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import resolve

from NewsPaper.settings import DEFAULT_FROM_EMAIL
from django.core.exceptions import PermissionDenied

from datetime import datetime, timedelta, timezone
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin,  PermissionRequiredMixin, UserPassesTestMixin # ограничение прав
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django.views.decorators.cache import cache_page # импортируем декоратор для кэширования отдельного представления
from django.core.cache import cache # импортируем наш кэш

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
    queryset = Category.objects.all()
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['category_sort'] = Post.objects.order_by('-id').filter(postCategory=self.kwargs['pk'])
        
        self.id = resolve(self.request.path_info).kwargs['pk'] # для подписки/отписки
        categ  = Category.objects.get(id=self.id)
        
                
        context['category_add'] = Category.objects.get(pk=self.kwargs['pk'])
        context['subscribers'] = categ.subscribers.all()  # подписчики
        context['category_one'] = categ.pk
        context['category']= categ  #categ.name
        return context


## для подписки и отписки по категориям
@login_required
def subCategory(request, pk):
    user = request.user
    # мой код работает
    #category_mail = Category.objects.get(pk=pk)
    category_mail = Category.objects.get(id=pk)
    
    # проверка точно ли юзер не подписан но у меня(проверка в html) получается двойная 
    #if not category_mail.subscribers.filter(id=user.id).exists():-проверка в html
    
    #category_mail.subscribers.add(request.user.id)-мой код
    category_mail.subscribers.add(user)
    
    # блок отправки на почту сообщения подписки
    email = user.email
       
    html_content = render_to_string (  'mail/newsmail_sub.html',
                                            {  'category_you': category_mail, # 'даем название использ в html' : 
                                                'user' : user,},               # чтобы в письме отразить имя пользов и категорию
                                        )
    msg = EmailMultiAlternatives(
            subject=f'Подтверждение подписки на раздел: - {category_mail}',#{category_mail.name} тема письма
            body='',
            from_email= DEFAULT_FROM_EMAIL, #так адрес возьмется из setting или прямо адрес писать 'petechka@yandex.ru',
            to=[email, ], # к email юзера через запятую можно добавить свою почту для проверки
    )
            
    msg.attach_alternative(html_content, "text/html") # (html, "text/html") добавляем html
    try:                # пытаемся отослать
            msg.send() # отсылаем  
    except Exception as e:
            print(e)
    #return redirect('edit')
    return redirect(request.META.get('HTTP_REFERER')) # возвращаемся назад на ту страницу с которой поступил запрос


@login_required
def unsubCategory(request, pk):
    user = request.user
    
    #category_mail = Category.objects.get(pk=pk) - мое решение работает
    #category_mail.subscribers.remove(request.user.id)

    category_mail = Category.objects.get(id=pk)  # видео решения
    
    # проверка точно ли юзер подписан но у меня(проверка в html)
    # if category_mail.subscribers.filter(id=user.id).exists():
    category_mail.subscribers.remove(user)
    
    # если хотим отправить письмо на почту при  отписке
    email = user.email
    html_content = render_to_string (  'mail/newsmail_unsub.html',
                                            {  'category_you': category_mail,
                                                'user' : user,},
                                        )
    msg = EmailMultiAlternatives(
            subject=f'Подтверждение отписки от раздела: - {category_mail.name}', # строка будет написана  в теме письма 
            body='',
            from_email=DEFAULT_FROM_EMAIL, #'petechka_admin@yandex.ru',
            to=[email],
        )
    msg.attach_alternative(html_content, "text/html") # добавляем html
    try:
            msg.send() # отсылаем  
    except Exception as e:
            print(e)

    #return redirect('edit')
    return redirect(request.META.get('HTTP_REFERER'))

# 

############

class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/one_news.html' 
    context_object_name = 'one_news'
    queryset = Post.objects.all()


    def get_object(self, *args, **kwargs): # переопределяем метод получения объекта,
        obj = cache.get(f'статья-{self.kwargs["pk"]}', None) # кэш очень похож на словарь, и метод get действует также. Он забирает значение по ключу, если его нет, то забирает None.
 
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset) 
            cache.set(f'статья-{self.kwargs["pk"]}', obj)
        
        return obj



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

# для ограничения постов использую сигналы
class AddNewsCreate( LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'flatpages/add_news.html' 
    form_class = AddNewsForm
    permission_required = ('news.add_post' )  

# второй способ ограничение по количеству постов
#class AddNewsCreate( LoginRequiredMixin,  PermissionRequiredMixin, CreateView):
    
#    template_name = 'flatpages/add_news.html' 
#    form_class = AddNewsForm
#    permission_required = ('news.add_post' ) 
    
   
#   def post(self, request):
#        form = self.form_class(request.POST, request.FILES) # request files для фото
#        if form.is_valid():
#           today=  timezone.datetime.now() - timedelta(days=1)
#            today= datetime.now()-timedelta(days=1)
#            author_user = Author.objects.get(authorUser_id =self.request.user.id)
#            allpost_day = Post.objects.filter(author=author_user, dataCreation__date=today).count()
#            if allpost_day > 3:
#                raise PermissionDenied ('Лимит постов')
#                return redirect('check_post.html')
#           #else:
#                form.save()
#                return redirect ('edit')
#        else:
#             return redirect('edit')
# 3 способ ограничение по количеству постов
#class AddNewsCreate( LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin, CreateView):
#    template_name = 'flatpages/add_news.html' 
#    form_class = AddNewsForm
#   permission_required = ('news.add_post' )           

   
    #def test_func(self):
        #author_user = Author.objects.get(authorUser_id =self.request.user.id)
        #today=  timezone.datetime.now() - timedelta(days=1)
        #allpost_day = Post.objects.filter(author=author_user, dataCreation__date=today).count()
       
        #if allpost_day > 3:
            #raise PermissionDenied ('Лимит постов')
                #return redirect('check_post.html')
        #else:
                
            #return redirect ('edit')
   
    





    
   
class NewsUpdateView(PermissionRequiredMixin, UpdateView):
        #model = Post
    template_name = 'flatpages/add_news.html' 
    
    form_class = AddNewsForm
    permission_required = ('news.change_post' )
    success_url = '/edit/'

         # метод get_object мы используем вместо queryset, 
         # чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
            
     


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    #model = Post
    template_name = 'flatpages/delete.html'
    queryset = Post.objects.all()
    permission_required = ('news.delete_post' )
    success_url = '/edit/'




def pageNotFound(request, exception):
   return HttpResponseNotFound('<h1>Страница не найдена</h1>')

# в этих функциях не уверена в правильности аргументов тут написала общий принцип исключений
def pageNotFound_500(request):
    return HttpResponseNotFound('<h1>Ошибка сервера</h1>')

def pageNotFound_403(request, exception):
    return HttpResponseNotFound('<h1>Нет доступа. Попробуйте позже</h1>')

#def pageNotFound_400(request, exception):
   # return HttpResponseNotFound('<h1>невозможно обработать запрос</h1>')

#def news(request):
   # return render(request, 'flatpages/news.html', {'title':'все новости'}) 


# каширование по функции
#@cache_page(60 * 15) # в аргументы к декоратору передаём количество секунд, 
# которые хотим, чтобы страница держалась в кэше. Внимание! Пока страница находится в кэше, изменения, происходящие на ней, учитываться не будут!
#def my_view(request):
#какая-то функция
