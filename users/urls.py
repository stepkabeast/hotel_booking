from django.urls import path
from booking import views
urlpatterns = [
 path('', views.home, name = "home"),
 path("signup/", views.SignUp.as_view(), name="signup"),
path('logout/', views.LogoutView.as_view(), name='logout'),
]