from django.contrib import admin
from django.urls import path
from salary.salaryapp.views import ObtainTokenView, SalaryView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', ObtainTokenView.as_view(), name='token_obtain'),
    path('api/salary/', SalaryView.as_view(), name='salary_view'),
]
