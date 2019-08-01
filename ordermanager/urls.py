from django.urls import path
from ordermanager import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/new/', views.CreateOrderView.as_view(), name='order_new'),
    path('order/<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order_edit'),
]
