from rest_framework import serializers
from .models import Worker


# класс WorkerSerializer, который является подклассом ModelSerializer из Django REST Framework.
# Тут модель Worker и поля, которые включитены в сериализацию.
class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('salary', 'date_of_grow')
