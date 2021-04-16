from django.urls import path
from . import views

app_name = 'cartt'

urlpatterns = [
    path('', views.cartt_detail, name='cartt_detail'),
    path('add/<int:product_id>/', views.cartt_add, name='cartt_add'),
    path('remove/<int:product_id>/', views.cartt_remove, name='cartt_remove'),
]