from django.contrib import admin

from .models import Women, Category

class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create','photo', 'is_published')
    list_filter = ('id', 'title') # активные поля для перехода к ним
    search_fields = ('title', 'content') #фильтр
    list_editable = ('is_published',) # делает редактируемы полк "Публикация"
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug':("title",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',) #ПОСТАВИТЬ ЗАПЯТУЮ, ПОТОМУ ЧТО ЭТО КОРТЕЖ!!!!
    prepopulated_fields = {'slug': ("name",)}

admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)