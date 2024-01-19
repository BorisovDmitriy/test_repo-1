import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm  # video 20 не надо написал свою форму
from django.contrib.auth.views import LoginView  # video 20
# from django.contrib.auth.forms import UserCreationForm # UserCreationForm  написали свою форму
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from rest_framework.authentication import TokenAuthentication


from .forms import *
from .models import *
from .permissions import IsAdminOrReadOnly
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator  # Видео 18

# DRF video2,3 и.т.д
from rest_framework import generics, viewsets
from .serializers import WomenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms import model_to_dict
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]

# Видео 17 убрал в utils.py для "mixina"
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
        # Video17 context['menu'] = menu
        # Video17 context['title'] = 'Главная страница'
        # Video17 context['cat_selected'] = 0
        # Video17 context['cats'] = Category.objects.all()
        c_def = self.get_user_context(title='Главная страница')  # видео 17
        return dict(
            list(context.items()) + list(c_def.items()))  # видео 17 забираем context из базового класса и миксина

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')


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
    return render(request, 'women/about.html', {'page_obj': page_obj, 'title': 'О сайте'})


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
    login_url = reverse_lazy(
        'home')  # сделаем что бы не вылазила ошибка 404 а было перенаправление на станицу регистрации
    raise_exception = True  # для генерации страницы 403 доступ запрещен

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))
        # Убрал из-зи миксина
        # context['title'] = 'Добавление статьи'
        # context['menu'] = menu
        # context['cats'] = Category.objects.all()
        # return context


# def contact(request): Видео 23
#     return HttpResponse("Обратная связь")

# Видео 23
class ContactFormView(DataMixin,
                      FormView):  # FormView стандартная форма, для представлений которые не взаимодействуют с БД
    form_class = ContactFormView
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):  # Этот метод вызывается в том случае если пользователь заполнил верно все поля формы
        print(form.cleaned_data)
        return redirect('home')


# def login(request):
#     return HttpResponse("Авторизация") Видео 20 убрал появилось нормальное представление


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
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # Оптимизируем запрос видео 21
        # c_def = self.get_user_context(title='Категория- ' + str(context['posts'][0].cat),
        #                               cat_selected=context['posts'][0].cat_id)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория- ' + str(c.name),
                                      cat_selected=c.pk)
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
    form_class = RegisterUserForm  # UserCreationForm написали свою форму
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Функция автоматической авторизации пользователя
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
    logout(request)  # Функция автоматической выхода пользователя с сайта
    return redirect('login')


class WomenAPIListPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page_size' # Указывается в адресной строке через амберсанд указывается количество страниц
    max_page_size = 10000 # Максимальное количество статей на странице


class WomenAPIList(generics.ListCreateAPIView): # Выводит список статей
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,) # Из за глобального ограничения указал в settings.py
    permission_classes = (IsAuthenticatedOrReadOnly,) # верул из-за видео 11
    pagination_class = WomenAPIListPagination


class WomenAPIUpdate(generics.RetrieveUpdateAPIView):  # Меняет определенную записб
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,) # Доступ в статью только с авторизацией по токену


class WomenAPIDestroy(generics.RetrieveDestroyAPIView):  # Удаляет статьи
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAdminOrReadOnly,)


# TODO Третий блок коментов видео 10
# class WomenViewSet(viewsets.ModelViewSet):
#     queryset = Women.objects.all() #Если убираем не забываем про basename в роутере
#     serializer_class = WomenSerializer
#
#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#
#         if not pk:
#             return Women.objects.all()[:3]
#         return Women.objects.filter(pk=pk) # только обязательно quweryset должен возвращать список поэтому ставим filter
#
#     @action(methods=['get'], detail=False) # Указываем метод, в данном случае только GET,detail-True будет отображаться только одна категория
#     def category(self,request):
#         cats = Category.objects.all()
#         return Response({'cats': [c.name for c in cats]})



    # @action(methods=['get'], detail=True)
    # def category(self,request, pk=None):
    #     cats = Category.objects.get(pk=pk)
    #     return Response({'cats': cats.name})



# # TODO Второй блок коментов из-за ViewSET
# class WomenAPIList(generics.ListCreateAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer
#
#
# class WomenAPIUpdate(generics.UpdateAPIView):
#     queryset = Women.objects.all() # В данном случае это ленивый запрос, не жадный. Поэтому вернется только изменяемая запись не все
#     serializer_class = WomenSerializer
#
#
# class WomenAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer

# TODO Первый блок коментов. Хуйня не нужная из-за классов,  за нас все написали уже давно
# class WomenAPIView(APIView):  # Наследуемся от самого главного класса
#     def get(self, request):
#         #Убрал после созд сериализатора lst = Women.objects.all().values() # без .values() будет вызван queryset и будет ошибка, нам нужен список
#         w = Women.objects.all()
#         return Response({'posts': WomenSerializer(w, many=True).data})  # папаметр many говорит программе,
#         # что нужно обрабатывать список значений, а не одну запись
#
#     def post(self, request):
#         serializer = WomenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # НЕ нужны из-за добавления метода save()
#         # post_new = Women.objects.create(
#         #     title=request.data['title'],
#         #     content=request.data['content'],
#         #     cat_id=request.data['cat_id'],
#         #     slug=request.data['slug'],
#         #     photo=request.data['photo']
#         # )
#
#         # return Response({'post': model_to_dict(post_new)})
#
#         #Причем после вызова метода save  не нужно вызывать новый объект сериализатора, а использовать тот что
#         # у нас есть и коллекция data будет ссылаться на новый созданый объект, тот который создаст метод create()
#         # return Response({'post': WomenSerializer(post_new).data}) # many по умолчанию False, потому что обрабатываем один объект
#         return Response({'post': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk',None)
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#
#         try:
#             instance = Women.objects.get(pk=pk)
#         except:
#             return Response({"error": "Method PUT not allowed"})
#
#         serializer = WomenSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"post": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"ERROR": "Delete Method Is Not Allowed"})
#         # deleting an object from api
#         try:
#             instance = Women.objects.get(pk=pk)
#             instance.delete()
#         except:
#             return Response({"ERROR": "Object Not Found !"})
#         return Response({"post": f"Object {str(pk)} is deleted"})


# class WomenAPIView(generics.ListAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer

