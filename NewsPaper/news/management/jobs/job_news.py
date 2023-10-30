
import datetime
from datetime import timedelta

from news.models import *

from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from NewsPaper.settings import DEFAULT_FROM_EMAIL


def week_catnews(): 
    template = 'mail/newsmail_weekpostcategory.html'
        # посты за период времени
    print('ggggg')
    for category in Category.objects.all():
        email_subject = f'Новые статьи в разделе: "{category} за неделю.'
        
        
        category_n = category.name
        category_m =category.id
       
        
            # собираем всех юзеров, которые подписаны на категории
        for user in category.subscribers.all():
            allpost_user=[]
                # посты за период времени
            time = datetime.now()-timedelta(weeks=1) #((second=50))
            post_week= Post.objects.filter(postCategory=category, dataCreation__gte= time, ) 
            allpost_user.extend(post_week)
            
         
            user_email=user.email
            user=user
       
            
            html = render_to_string(
                    template_name = template,
                    context = {
                        'category_m':category_m,
                        'category_adduser': category_n,
                        'post_foruser': post_week,
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




def week_catnews_1(): 
    template = 'mail/newsmail_weekpostcategory.html'
        # посты за период времени
    print('ggggg')
    for category in Category.objects.all():
        email_subject = f'Новые статьи в разделе: "{category} за неделю.'
        
        
        category_n = category.name
        category_m =category.id
       
        
            # собираем всех юзеров, которые подписаны на категории
        for user in category.subscribers.all():
            allpost_user=[]
                # посты за период времени
            time = datetime.now()-timedelta(weeks=1) #((second=50))
            post_week= Post.objects.filter(postCategory=category, dataCreation__gte= time, ) 
            allpost_user.extend(post_week)
            
         
            user_email=user.email
            user=user
       
            
            html = render_to_string(
                    template_name = template,
                    context = {
                        'category_m':category_m,
                        'category_adduser': category_n,
                        'post_foruser': post_week,
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






