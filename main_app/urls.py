from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('', views.home, name="home"),
  path('about/', views.about, name="about"),
  path('accounts/signup/', views.signup, name="signup"),
  path('profile/', views.profile, name="profile"),
  path('profile/<int:user_id>/', views.view_profile, name="view_profile"),
  path('profile/edit/', views.edit_profile, name="edit_profile"),
  path('event/<str:event_name>/', views.event_detail, name="event_detail"),
  path('search/', views.search_bar, name="search"),
  path('search/by_category/', views.filter, name="filter"),
  path('event/<int:event_id>/register/', views.event_register, name="event_register"),
  path('change-password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html', success_url='/'), name='change-password'),
]