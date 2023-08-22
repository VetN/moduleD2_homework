from django.contrib import admin
from .models import Category, Author, Post, PostCategory, Comment
 
 



#admin.site.unregister(Product) # разрегистрируем наши товары


# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ["title", "Author"] # генерируем список имён всех полей для более красивого отображения



admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comment)