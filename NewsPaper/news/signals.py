from datetime import datetime 

from news.tasks.basic import new_post_subscription
#from news.tasks.basic import new_post_subscription_1
from .models import Post
from django.dispatch import receiver
from django.core.exceptions import PermissionDenied
from django.db.models.signals import post_save, m2m_changed # вызываем именно промежуточную модель с помощью (m2m_changed)

# необходимо прописать в арр.ру если используем сигналы в отдельном файле,
# обязательно проаисать в setting

# сигнал на добавление поста в категорию
# сигнал если в категории появляется пост, то сраб функция instance - данные этого конкретного добавленного сейчас поста
@receiver(m2m_changed, sender = Post.postCategory.through) # sender = PostCategory декоратор который помогает функции отработать по сигналу
def notify_subscribers(sender, instance, action, **kwargs): # instance(экземпляр postcategory)
    if action == 'post_add': # проверяем именно действие action( что именно создание а не редактирование)
      new_post_subscription(instance)
      #new_post_subscription_1(instance)- второй вариант функция работает через список


# сигнал на добавление в сутки больше скольки-то постов
@receiver(post_save, sender = Post) # sender = Postдекоратор который помогает функции отработать по сигналу
def   all_post(sender, instance,  **kwargs): # instance(экземпляр postcategory)
 
      #today = datetime.now()
      today = datetime.today()
      allpost_day = Post.objects.filter(author=instance.author, dataCreation__date=today).count()
      if allpost_day >3:
         
        instance.delete()
        raise PermissionDenied # выводится текст 403 ошибки
    