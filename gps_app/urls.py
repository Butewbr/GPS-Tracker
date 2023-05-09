from django.urls import path
from .views import receive_data, show_data

urlpatterns = [
    path('receive-data/', receive_data, name='receive_data'),
    path('show-data/', show_data, name='show_data'),
]
