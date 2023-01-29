from django.urls import path, include
from . import views

app_name = 'pins'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.pins_feed, name='pins_feed'),
    path('fetch/', views.fetch_suggestions, name='fetch_suggestions'),
    path('search/<slug:slug>/', views.search, name='search'),
    path('create/', views.pins_create, name='pins_create'),
    path('save/', views.pins_save, name='pins_save'),
    path('detail/<int:id>/<slug:slug>/', views.pins_detail, name='pins_detail'),
    path('comment/', views.pins_comment, name='pins_comment'),
]