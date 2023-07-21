import datetime

from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import *

# menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]

# menu = [{'title': "О сайте", 'url_name': 'about'},                # видео 11 добавили свой тег чбобы выполнить требоване DRY ООП
#         {'title': "Добавить статью", 'url_name': 'add_page'},
#         {'title': "Обратная связь", 'url_name': 'contact'},
#         {'title': "Войти", 'url_name': 'login'}
# ]


def index(request): #HttpRequest название любое, сылка на request обязательна
    posts = Women.objects.all()
    # cats = Category.objects.all() видео 11 добавили свой тег чбобы выполнить требоване DRY ООП
    context = {'posts': posts,
              # 'cats': cats, видео 11 добавили свой тег чбобы выполнить требоване DRY ООП
              #  'menu': menu, видео 11 добавили свой тег чбобы выполнить требоване DRY ООП
               'title': 'Главная страница',
               # 'cat_selected': 0,
                }
    return render(request, 'women/index.html',context=context)


def about(request): #HttpRequest название любое, сылка на request обязательна
    context = {'title': 'О сайте'}
    return render(request, 'women/about.html', context=context) # Изменил из-за списка menu


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data) #запись в терминале
            # try:
                #Women.objects.create(**form.cleaned_data)
                form.save()
                return redirect('home')
            # except:
            #     form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddPostForm()
    return render(request, 'women/addpage.html', {'form': form, 'title': 'Добавление статьи',})

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")



def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# def show_post(request, post_id):
#     post = get_object_or_404(Women, pk=post_id) # маршрут по слагу

def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    context = {
        'post': post,
        # не добавлял menu
        'title': post.title,


    }
    return render(request, 'women/post.html', context=context)


def show_category(request, cat_slug):
    cat = Category.objects.get(slug=cat_slug)
    posts = Women.objects.filter(cat_id=cat.pk)
    # cats = Category.objects.all() видео 11 добавили свой тег чбобы выполнить требоване DRY ООП
    if len(posts) == 0:
        raise Http404()

    context = {'posts': posts,
               #'cats': cats, видео 11 добавили свой тег чбобы выполнить требоване DRY ООП
               # 'menu': menu, видео 11 добавили свой тег чбобы выполнить требоване DRY ООП
               'title': 'Отображение по рубрикам',
               'cat_selected': cat.pk,
               }
    return render(request, 'women/index.html', context=context)



