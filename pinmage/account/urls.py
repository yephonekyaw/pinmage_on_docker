from django.urls import path, include
from . import views

app_name = 'account'

urlpatterns = [
    path('follow/', views.user_follow, name='user_follow'),
    path('edit/', views.user_profile_edit, name='user_profile_edit'),
    path('<username>/', views.user_profile, name='user_profile'),
]