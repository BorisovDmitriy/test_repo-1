from django.db.models import Count

from .models import Category
menu = [{'title': "О сайте", 'url_name': 'about'},  # видео 11 добавили свой тег, чтобы выполнить требование DRY ООП
        # видео 15 вернул для классов
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        #{'title': "Войти", 'url_name': 'login'}# Видео 19
        ]

class DataMixin:
    paginate_by = 2
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('women'))
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
