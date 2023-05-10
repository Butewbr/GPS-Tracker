from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('receive-data/', views.receive_data, name='receive_data'),
    path('show-data/', views.show_data, name='show_data'),
]
