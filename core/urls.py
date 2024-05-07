from django.urls import path
from core.views import HomeView, IndexHomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'), 
    path('home-auth/', IndexHomeView.as_view(), name='home-auth'), 
]
