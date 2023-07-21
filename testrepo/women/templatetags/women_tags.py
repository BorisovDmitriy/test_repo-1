from django import template
from women.models import *

register = template.Library()

# Простой тег
@register.simple_tag(name='getcat')
def get_categoryes(filter=None): # Называем ка хотим
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)



# Включающие теги
@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None,  cat_selekted=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats': cats, 'cat_selected': cat_selekted, }


@register.inclusion_tag('women/list_menu.html')
def list_menu():
    menu = [{'title': "О сайте", 'url_name': 'about'},
            {'title': "Добавить статью", 'url_name': 'add_page'},
            {'title': "Обратная связь", 'url_name': 'contact'},
            {'title': "Войти", 'url_name': 'login'}
            ]
    return {'menu': menu}