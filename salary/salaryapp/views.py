from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from salary.salaryapp.models import Worker
from rest_framework import exceptions

from salary.salaryapp.serializers import WorkerSerializer

# представление SalaryView, которое является подклассом APIView из Django REST Framework.
# Установливаем permission_classes в [IsAuthenticated], чтобы требовать аутентификации для доступа к этому представлению.
# В методе get получаем объект сотрудника, связанного с текущим пользователем (request.user), сериализуем его с помощью WorkerSerializer
# и возвращаем данные в формате JSON с помощью Response.
class SalaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        worker = Worker.objects.get(user=request.user)
        serializer = WorkerSerializer(worker)
        return Response(serializer.data)

# Представление ObtainTokenView, которое является подклассом APIView из Django REST Framework.
# Метод post обрабатывает запросы на аутентификацию.
# Мы проверяем переданные логин и пароль с помощью authenticate из модуля django.contrib.auth.
# Если аутентификация проходит успешно, создаем токен доступа и токен обновления с помощью RefreshToken.for_user(user).
# Затем возвращаем ответ с токенами в формате JSON.
class ObtainTokenView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credit'}, status=401)

#класс CustomJWTAuthentication, который наследуется от JWTAuthentication из rest_framework_simplejwt.authentication.
# Переопределяем метод has_permission, чтобы проверить, существует ли для текущего пользователя связанный сотрудник в модели Worker.
# Если сотрудник не существует, выбрасываем исключение PermissionDenied.
class CustomJWTAuthentication(JWTAuthentication):
    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            return False

        try:
            worker = Worker.objects.get(user=request.user)
            return True
        except Worker.DoesNotExist:
            raise exceptions.PermissionDenied('Нет доступа')