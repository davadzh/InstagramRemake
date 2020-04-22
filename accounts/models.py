from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Profile_info(models.Model):
    username = models.OneToOneField(User, default=1, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank='True')
    phone = models.CharField(max_length=50, null=True, blank='True')
    email = models.CharField(max_length=50, null=True, blank='True')
    profile_pic = models.ImageField(null=True, blank=True, default='default.png')
    subscribers = models.ManyToManyField(User, blank='True', related_name='subscribers')
    subscriptions = models.ManyToManyField(User, blank='True', related_name='subscriptions')

    def __str__(self):
        return self.username.username


class Notification(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_from = models.CharField('Другой пользователь', max_length=300, blank=True)
    notification_text = models.CharField('Текст уведомления', max_length=300, blank=True)
    pub_id = models.IntegerField('Идентефикатор публикации', null=True, blank=True)
    not_date = models.DateTimeField('Дата уведомления', auto_now_add=True)

    def __str__(self):
        return self.notification_text




class Publication(models.Model):
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    pub_text = models.TextField('Введите текст публикации')
    pub_pic = models.ImageField('Загрузите фото', null=True)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    pub_likes = models.ManyToManyField(User, blank='True', related_name='post_likes')

    def total_likes(self):
        return self.pub_likes.count() 

    #  auto_now_add=True

    def __str__(self):
        return self.pub_text


    
class Comment(models.Model):
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    pub = models.ForeignKey(Publication, on_delete=models.CASCADE)
    comment_text = models.TextField('Введите текст ...')
    comment_date = models.DateTimeField('Дата комментария', auto_now_add=True)

    def __str__(self):
        return self.comment_text