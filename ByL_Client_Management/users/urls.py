from django.urls import path
from .views import bylLoginView, bylLogoutView

urlpatterns = [
    path('login/', bylLoginView.as_view(), name='login'),
    path('logout/', bylLogoutView.as_view(), name='logout'),
]