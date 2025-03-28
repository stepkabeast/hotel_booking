from django.urls import path
from booking import views
urlpatterns = [
 path("signup/", views.SignUp.as_view(), name="signup"),
 path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
]