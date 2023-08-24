from django.db import models

# Create your models here.

class Posts(models.Model):
    title = models.CharField('Название', max_length=50)
    text = models.TextField('Текст')
    date = models.DateTimeField('Дата публикации', auto_now_add=True)
    editDate = models.DateTimeField('Дата редактирования',null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Theme(models.Model):
    ip = models.TextField('ip')
    theme = models.TextField('тема')

    def __str__(self):
        return self.ip
    
    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'