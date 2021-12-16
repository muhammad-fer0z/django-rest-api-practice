from django.urls import path
from .views import IncomeListApiView, IncomeDetailApiView

urlpatterns = [
    path('', IncomeListApiView.as_view(), name='income-list'),
    path('<int:id>/', IncomeDetailApiView.as_view(), name='income-detail'),
]
