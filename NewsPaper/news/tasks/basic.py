#import email
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
#from news.models import User
from django.conf import settings
from NewsPaper.settings import DEFAULT_FROM_EMAIL
# cюда пишем функции для сигналов, т.е. те, которые должны срабатывать при опред условиях
# функция при появления поста отправляется письмо
# эта функция может срабатываться через сигнал или
# (что лучше) прописать ее в class AddNewsCreate( CreateView)
# 2 способа

# 1 способ
# функция рассылки уведомления на почту при добавлении новой статьи в категории
# так делаю, если хочу, чтобы рассылка шла не списком, а персональная
# это дает возможность обратиться к подписчику по имени
# и получить другие данные юзера 
# функция передана в signals.py работают оба варианта включаются там
def new_post_subscription(instance):
    template = 'mail/newsmail_addpostcategory.html'
    for category in instance.postCategory.all():
        #email_subject = f'Новый пост в категории: "{category}"'
        email_subject = f'Новый пост в категории: "{category} от автора {instance.author.authorUser.first_name}'
        for user in category.subscribers.all():
            user_email=user.email
            user=user
            html = render_to_string(
                template_name = template,
                context = {
                    'category_adduser': category,
                    'post_foruser': instance,
                    'user': user,

                    },
                )
            msg = EmailMultiAlternatives(
                    subject= email_subject,
                    body='',
                    from_email= DEFAULT_FROM_EMAIL,
                    to = [user_email,]
                    

            )
            msg.attach_alternative(html, 'text/html')
            msg.send()

# 2 способ
# так делаю, если хочу просто рассылку всем сразу
# но тут нет возможности получить персональные данные по юзеру
# так как формируется список емайл и на них идет рассылка
# создаем функцию занесения в общий список email-ов всех юзеров подписанных на данную категорию 
def get_subscribers(category):
    user_email = []
    for user in category.subscribers.all():
        user_email.append(user.email)
    return user_email

def new_post_subscription_1(instance):    
    template = 'mail/newsmail_addpostcategory.html'
    email_subject = f'Создание поста: {instance.title} от автора {instance.author.authorUser.first_name}'
    
    for category in instance.postCategory.all():
    
        email_users = get_subscribers(category)
        html = render_to_string(
            template_name = template,
            context = {
                'category_adduser': category,
                'post_foruser': instance,
               
                },
            )
        msg = EmailMultiAlternatives(
            subject = email_subject,
            body = '',
            from_email = settings.DEFAULT_FROM_EMAIL,
            to = email_users,
            )
        msg.attach_alternative(html, "text/html")
        msg.send()
