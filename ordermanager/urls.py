from django.urls import path
from ordermanager import views

urlpatterns = [
    path('about/', views.AboutView.as_view(), name='about'),
]
