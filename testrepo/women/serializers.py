import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Women

class WomenSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Women
        fields = ('title', 'slug', 'content', 'cat', 'user')
        # если хотите чтобы передавались все поля то надо вписать "__all__"
        # fields = "__all__"

#TODO все это можно было написать тремя строчками чрез наследоване у ModelSerializer

# class WomenSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     content = serializers.CharField()
#     slug = serializers.SlugField(max_length=255)
#     time_create = serializers.DateTimeField(read_only=True)
#     time_update = serializers.DateTimeField(read_only=True)
#     is_published = serializers.BooleanField(default=True)
#     cat_id = serializers.IntegerField()  #  Обратить внимание что тут выбрали числое значение
#     # хоть в модели указан ForengyKEy, потому что на выход будет транслироваться число для JSON строки
#     photo = serializers.ImageField(read_only=True)
#
#     def create(self, validated_data):
#         return Women.objects.create(**validated_data) # словарь распаковывается
#
#     def update(self, instance, validated_data): # instance сылка на объект Women, validated_data -ссыдка на словарь
#         instance.title = validated_data.get('title', instance.title)
#         instance.content = validated_data.get('content', instance.content)
#         instance.slug = validated_data.get('slug', instance.slug)
#         instance.time_update = validated_data.get('time_ipdate', instance.time_update)
#         instance.is_published = validated_data.get('is_published', instance.is_published)
#         instance.cat_id = validated_data.get('cat_id', instance.cat_id)
#         instance.photo = validated_data.get('photo', instance.photo)
#         instance.save()
#         return instance
#
#     def delete(self, instance):
#         return Women.objects.delete(instance)

# Это пример описывающий работу сериализатора
# class WomenModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content


# Это пример описывающий работу сериализатора
# def encode():
#     model = WomenModel('Angelina Jolie', 'Content: Angelina Jolie')
#     model_sr = WomenSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
# Это пример описывающий работу сериализатора
# def decode():
#     stream = io.BytesIO(b'{"title":"Angelina Jolie","content":"Content: Angelina Jolie"}')
#     data = JSONParser().parse(stream)
#     serializer = WomenSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)