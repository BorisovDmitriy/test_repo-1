# python manage.py shell

from women.models import Women


def todo():
    # полезно для отладки удалять объекты
    Women.objects.all().delete()

Women(title='Анджелина Джоли', content='Биография Анджелины Джоли' )
w1=_
w1.save()
w2 = Women(title='Dima', content='Биография Димы')