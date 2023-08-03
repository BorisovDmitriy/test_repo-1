import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm # video 20 не надо написал свою форму
from django.contrib.auth.views import LoginView # video 20
# from django.contrib.auth.forms import UserCreationForm # UserCreationForm  написали свою форму
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .forms import *
from .models import *
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator # Видео 18


# menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]

# Видео 17 убрал в utils.py для mixina
# menu = [{'title': "О сайте", 'url_name': 'about'},
# видео 11 добавили свой тег, чтобы выполнить требование DRY ООП
#         # видео 15 вернул для классов
#         {'title': "Добавить статью", 'url_name': 'add_page'},
#         {'title': "Обратная связь", 'url_name': 'contact'},
#         {'title': "Войти", 'url_name': 'login'}
#         ]


class WomenHome(DataMixin, ListView):
    # paginate_by = 3  # Видео №18 добавление пагинации, убрал в миксин
    model = Women  # указываем модель, объекты которой мы будем выводить
    template_name = 'women/index.html'
    # указываем имя шаблона, где будет лежать HTML, в котором будут все инструкции о том,
    # как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'

    # это имя списка, в котором будут лежать все объекты,
    # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    # extra_context = {'title': 'Главная страница'} Первый способ передачи атрибутов Статических

    # общий метод для создания дополнительных атрибутов, добавить атрибуты в html
    # Это формирование дина динамического контекста
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # обращаемся к базовому классу для получения уже сформированных
        # атрибутов например context_object_name = 'posts'. Чтобы ничего не потерять
        #Video17 context['menu'] = menu
        #Video17 context['title'] = 'Главная страница'
        #Video17 context['cat_selected'] = 0
        #Video17 context['cats'] = Category.objects.all()
        c_def = self.get_user_context(title='Главная страница') # видео 17
        return dict(list(context.items()) + list(c_def.items())) # видео 17 забираем context из базового класса и из миксина

    def get_queryset(self):
        return Women.objects.filter(is_published=True)


# видео 15 перешли на классы
# def index(request): #HttpRequest название любое, ссылка на request обязательна
#     posts = Women.objects.all()
#     # cats = Category.objects.all() видео 11 добавили свой тег чтобы выполнить требование DRY ООП
#     context = {'posts': posts,
#               # 'cats': cats, видео 11 добавили свой тег чтобы выполнить требование DRY ООП
#               #  'menu': menu, видео 11 добавили свой тег чтобы выполнить требование DRY ООП
#                'title': 'Главная страница',
#                # 'cat_selected': 0,
#                 }
#     return render(request, 'women/index.html',context=context)

@login_required
def about(request):  # HttpRequest название любое, ссылка на request обязательна
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'women/about.html',{'page_obj': page_obj, 'title': 'О сайте'})




# Видео 15 перешли на классы
# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data) #запись в терминале
#             # try:
#             # Women.objects.create(**form.cleaned_data)
#             form.save()
#             return redirect('home')
#         # except:
#         #     form.add_error(None, 'Ошибка добавления поста')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'title': 'Добавление статьи', })

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home') #сдлаем что бы не вылазила ошибка 404 а было перенаправление на станицу регистрации
    raise_exception = True  # для генерации страницы 403 доступ запрещен

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items() + list(c_def.items())))
        # Убрал из-зи миксина
        # context['title'] = 'Добавление статьи'
        # context['menu'] = menu
        # context['cats'] = Category.objects.all()
        # return context



def contact(request):
    return HttpResponse("Обратная связь")


# def login(request):
#     return HttpResponse("Авторизация") Видео 20 убрал повилось нормпльное представление


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# def show_post(request, post_id):
#     post = get_object_or_404(Women, pk=post_id) # было по id\pk стал маршрут по слагу

# Видео 15 перешли на классы
# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context = {
#         'post': post,
#         # не добавлял menu
#         'title': post.title,
#     }
#     return render(request, 'women/post.html', context=context)


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'
    # pk_url_kwarg =  'post_pk' к примеру это если не по слагу,  а по id принимает

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))
        # Убрал из-зи миксина
        # context['title'] = context['post']
        # context['menu'] = menu
        # context['cats'] = Category.objects.all()
        # return context


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    # здесь мы выбираем категорию по указанному слагу и публикацией True,
    # cat__slug -мы обращаемся к полю cat, через которою обращаемся к полю slug модели Category и забираем его
    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория- ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))
        # Видео 17 миксин
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)  # мы обращаемся к коллекции posts,
        # # которую задали выше обращаемся к первой записи [0] и забираем параметр cat, и преобразованная строка
        # # плюсуется к слову категория и отображается в title
        # context['menu'] = menu
        # context['cat_selected'] = context['posts'][0].cat.id  # здесь то же самое
        # context['cats'] = Category.objects.all()
        # return context

# Видео 15 перешли на классы
# def show_category(request, cat_slug):
#     cat = Category.objects.get(slug=cat_slug)
#     posts = Women.objects.filter(cat_id=cat.pk)
#     cats = Category.objects.all() #видео 11 добавили свой тег чтобы выполнить требование DRY ООП
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {'posts': posts,
#                'cats': cats, #видео 11 добавили свой тег чтобы выполнить требование DRY ООП, вернул из за видео 15
#                'menu': menu, #видео 11 добавили свой тег чтобы выполнить требование DRY ООП
#                             # вернул видео 15
#                'title': 'Отображение по рубрикам',
#                'cat_selected': cat.pk,
#                }
#     return render(request, 'women/index.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm # UserCreationForm написали свою форму
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user) #Функция автомвтической авторизации пользователя
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    # def get_success_url(self):
    #     return reverse_lazy('home')  # добавил в settings LOGIN_REDIRECT_URL = '/'


def logout_user(request):
    logout(request) #Функция автомвтической выхода пользователя с сайта
    return redirect('login')

