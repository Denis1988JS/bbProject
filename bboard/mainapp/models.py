from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

#Модель пользователя - собственная от производной
class AbvUser(AbstractUser):
    is_activated = models.BooleanField(default=True,db_index=True, verbose_name='Активация пользователя')
    send_messages = models.BooleanField(default=True, verbose_name='Оповещения о новых комментариях')
    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(self, *args, **kwargs)
    class Meta(AbstractUser.Meta):
        pass

#Модель рубрики
class Rubric(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название рубрики')
    order = models.IntegerField(default=0, db_index=True, verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT,null=True, blank=True, verbose_name='Надрубрика')
    def __str__(self):
        return self.name
    class Meta:
         verbose_name = 'Рубрика'
         verbose_name_plural = 'Рубрики'
         ordering = ['id']

#Модель надрубрик
class SuperRubricManager(models.Manager):
    def get_queryser(self):
       return super(SuperRubricManager, self).get_queryser().filter(super_rubric__isnull=True)

class SuperRubric(Rubric):
    object = SuperRubricManager()
    class Meta:
        proxy =True
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'
        ordering = ['id', 'name']

#Модель подрубрика
class SubRubricManager(models.Manager):
    def get_queryser(self):
       return super(SubRubricManager, self).get_queryser().filter(super_rubric__isnull=False)

class SubRubric(Rubric):
    object = SubRubricManager()
    def __str__(self):
        return ( self.name)
    class Meta:
        proxy =True
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'
        ordering = ['id', 'name','super_rubric__order','super_rubric__name']


#Модели - объявления
class Bb(models.Model):
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Рубрика')
    title = models.CharField(max_length=100, verbose_name='Название товара')
    content = models.TextField(max_length=10000,verbose_name='Описание товара')
    price = models.IntegerField(default=0, verbose_name='Цена')
    contacts = models.TextField(max_length=500, verbose_name='Контакты')
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', verbose_name = 'Изображение')
    autor = models.ForeignKey(AbvUser, on_delete=models.CASCADE, verbose_name='Автор объявления')
    is_avtive = models.BooleanField(default=True, db_index=True, verbose_name='Выводить объявление')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args,**kwargs)
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-create_date']

#Модель - много фото к объявлению
class AdditionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Объявление')
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', verbose_name = 'Изображение')
    class Meta:
        verbose_name = 'Дополнительная иллюстрация'
        verbose_name_plural = 'Дополнительные иллюстрации'

#Модель Комментарий к объявлению

class Comment(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Объявление')
    autor = models.CharField(max_length=30, verbose_name='Автор')
    content = models.TextField(max_length=5000, verbose_name='Содержание')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Отобразить комментарий')
    created_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_time']


