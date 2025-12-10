from django.urls import path
from . import views


urlpatterns = [
    path('movements/', views.stock_movement_list, name='stock_movement_list'),
]
