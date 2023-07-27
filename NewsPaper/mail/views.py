from django.contrib.auth.decorators import login_required
from news.models import Category
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect


@login_required
def subCategory(request, pk):
    user = request.user
    category_mail = Category.objects.get(id=pk)
    
    if not category_mail.subscribers.filter(id=user.id).exists():
        category_mail.subscribers.add(user.id)
        email = user.email
        # загруж шаблон и вызыв метод render
        html_content = render_to_string (  'mail/newsmail.html',
                                            {  'categories': category_mail,
                                                'user' : user,
                                            },
                                        )
        msg = EmailMultiAlternatives(
            subject=f'Подтверждение подписи на категорию - {category_mail.name}',
            body='',
            from_email='vet.nes@yandex.ru',
            to=[email, 'vetaness@mail.ru'], # пишу свою почту для проверки
        )
        msg.attach_alternative(html_content, "text/html") # добавляем html
        try:
            msg.send() # отсылаем  
        except Exception as e:
            print(e)
        return redirect('edit')
    return redirect(request.Meta.get('HTTP_REFERER'))


@login_required
def unsubCategory(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user.id)
    return redirect('edit')