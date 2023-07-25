

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# для группы премиум
from django.shortcuts import redirect 
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from news.models import *

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index_user.html'# Create your views here.
        
        
            # определение есть ли пользователь в группе
            # получаем весь контекст
            # exists() выберет из всего контекста пользователя со всеми его группами если есть премиум
            # но not переворачивает наоборот
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name = 'premium').exists()
        return context
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context
# Добавляем функциональное представление в группу премиум

@login_required # декоратор проверки аунтентификации
def upgrade_me(request):
   user = request.user
   premium_group = Group.objects.get(name='premium')
   if not request.user.groups.filter(name='premium').exists():
       premium_group.user_set.add(user)
       
   return redirect('/')

@login_required # декоратор проверки аунтентификации
def upauthors(request):
   user = request.user
   authors_group = Group.objects.get(name='authors')
   if not request.user.groups.filter(name='authors').exists():
       authors_group.user_set.add(user)
       Author.objects.create(authorUser=user)
   return redirect('edit')