from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

from django.core.cache import cache

# Create your models here.
class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete = models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)
    
    def __str__(self):
        return self.authorUser.first_name
    

    def update_rating(self):
        #postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
        #pRat = 0
        #pRat += postRat.get('postRating')

        #commentRat = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
        #cRat = 0
        #cRat += commentRat.get('commentRating')
        
        postRat = self.post_set.all().aggregate(postRat=Sum('rating'))['postRat'] or 0
        commentRat = self.authorUser.comment_set.all().aggregate(commentRat=Sum('rating'))['commentRat'] or 0
        self.ratingAuthor = postRat * 3 + commentRat
        self.save()



class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, blank=True) # юзары по категориям
    
    def __str__(self):
        return self.name
        #return f'{self.name.title()}'

class Post(models.Model):
   
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE ='AR'
    CATEGORY_CHOICES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    ]
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES,  default=ARTICLE)
    dataCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)
    photo = models.ImageField(upload_to = 'image_photo/', blank=True, null=True,  )

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

        # функция возращает только часть контента
    def preview(self):
        return self.content[0:100] + '...'
    
    def __str__(self):
        return self.title
    
    #def __str__(self):
        return self.postCategory.Category.name
    
    def get_category_type(self):
        return self.get_categoryType_display()
    
    def get_absolute_url(self): # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'
        # промежуточна модель, связывающая 2 модели Post и Category

    # для кеша если в класса добавлен метод переопределения
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'статья-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post,on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    dataCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.commentUser.username 
        
