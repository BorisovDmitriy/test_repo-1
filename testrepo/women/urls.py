from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', WomenHome.as_view(), name='home'), # http://127.0.0.1:8000
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    # path('post/<int:post_id>/', show_post, name='post'), Видео 12 добавили поиск по slug
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),

    # path('cats/<int:catid>', categories), # http://127.0.0.1:8000/cats/1
    # re_path(r'^archive/(?P<year>[0-9]{4})/', archive),  # http://127.0.0.1:8000/archive/2020/
]