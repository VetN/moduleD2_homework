from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import RegisterForm

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .forms import *
class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'sign/signup.html'
    success_url = '/'
            
            
            # автоматическое подключение к группе без использования allauth
            # group = Group.objects.get(name='my_group') 
            # Обращаемся к БД, находим нужную группу. Может оказаться, что такой группы в БД нет. 
            # Тогда получим ошибку. Надёжнее использовать метод get_or_create. 
            # Обратите внимание, что этот метод возвращает кортеж, 
            # поэтому мы обращаемся к первому элементу кортежа через скобки.
    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get_or_create[1]
        user.groups.add(group) # добавляем нового пользователя в эту группу
        user.save()
        return super().form_valid(form)

    def sellHi(request):
        user = request.user
        email = user.email
        # блок отправки подтверждения подписки
        html_content = render_to_string (  'mail/newsmail_hi.html',
                                            {  'user' : user,},
                                        )
        msg = EmailMultiAlternatives(
                subject=f'Приветственное письмо от MainNews',
                body='',
                from_email='vet.ness@yandex.ru',
                to=[email], # пишу свою почту для проверки
                )
        msg.attach_alternative(html_content, "text/html") # добавляем html
        try:
            msg.send() # отсылаем  
        except Exception as e:
            print(e)
        return redirect('edit')



class LoginView(FormView):
    model = User
    form_class = LoginForm
    template_name = 'sign/login.html'
    success_url = '/edit/'
  
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request,username=username, password=password)
        if user is not None:
           login(self.request, user)
        return super().form_valid(form)
  
  
class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/logout.html'
    
   
    def get(self, request, *args, **kwargs):
       logout(request)
       return super().get(request, *args, **kwargs)
   
