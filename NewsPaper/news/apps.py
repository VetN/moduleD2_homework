from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    
    def ready(self):
        import news.signals
      
        
        # нам надо переопределить метод ready, 
 # чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками