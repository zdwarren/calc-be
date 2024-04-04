from django.urls import path
from .views import CalculationListCreate, CalculationDetail

urlpatterns = [
    path('calculations/', CalculationListCreate.as_view(), name='calculation-list-create'),
    path('calculations/<int:pk>/', CalculationDetail.as_view(), name='calculation-detail'),
]
