from django.urls import path
from . import views


urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('create/', views.order_create, name='order_create'),
    path('<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('<int:pk>/confirm/', views.order_confirm, name='order_confirm'),
    path('<int:pk>/cancel/', views.order_cancel, name='order_cancel'),
    path('<int:order_pk>/items/add/', views.order_item_add, name='order_item_add'),
    path('<int:order_pk>/items/<int:item_pk>/remove/', views.order_item_remove, name='order_item_remove'),
]
