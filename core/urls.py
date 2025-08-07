from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book_ride, name='book'),
    path('contact/', views.contact, name='contact'),
]