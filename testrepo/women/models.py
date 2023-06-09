from django.db import models
from django.urls import reverse
# Create your models here.
class Women(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")# Размещать фото будем в каталог, опредилим его
                                                            # с помощью шаблона  с описанием года/месяца/дня
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT,null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ('post', kwargs={'post_id': self.pk})

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)# db_index говрит нам о томб
    # что поле будет индексировано и поиск будет происходить быстрее

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse ('category', kwargs={'cat_id': self.pk})