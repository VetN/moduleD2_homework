from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.
class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete = models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)
  
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

class Post(models.Model):
   
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE ='AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dataCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

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
        
# Create your models here.
