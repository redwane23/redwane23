from django.urls import path
from account import views
from .views import CustomLoginView
urlpatterns = [
    path("create_account/",views.create_account,name='register'),
    path("login/",CustomLoginView.as_view(),name='login'),
]
