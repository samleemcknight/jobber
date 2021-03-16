from django.urls import path
from . import views 

urlpatterns = [
  path('', views.home, name="home"),
  path('accounts/signup/', views.signup, name="signup"),
  path('event/<int:event_id>/', views.event_detail, name="event_detail"),
]