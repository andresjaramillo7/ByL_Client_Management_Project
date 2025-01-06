from django.urls import path
from . import views

urlpatterns = [
    path('', views.promotion_list, name='promotion_list'),
    path('create/', views.create_promotion, name='create_promotion'),
    path('edit/<int:promotion_id>/', views.edit_promotion, name='edit_promotion'),
    path('delete/<int:promotion_id>/', views.delete_promotion, name='delete_promotion'),
]