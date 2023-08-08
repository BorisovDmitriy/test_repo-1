from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Women, Category


class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')
    list_filter = ('id', 'title')  # активные поля для перехода к ним
    search_fields = ('title', 'content')  # фильтр
    list_editable = ('is_published',)  # делает редактируемы полк "Публикация"
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ("title",)}
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create',
              'time_update')  # video 24
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')  # video 24
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Миниатюра"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)  # ПОСТАВИТЬ ЗАПЯТУЮ, ПОТОМУ ЧТО ЭТО КОРТЕЖ!!!!
    prepopulated_fields = {'slug': ("name",)}


admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админ-панель сaйта о женщинах'  # video 24
admin.site.site_header = 'Админ-панель сaйта о женщинах 2'
