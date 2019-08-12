from django.urls import path
from ordermanager import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/new/', views.CreateOrderView.as_view(), name='order_new'),
    path('order/<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order_edit'),
    path('contacts/', views.ContactListView.as_view(), name='contact_list'),
    path('contact/<int:pk>', views.ContactDetailView.as_view(), name='contact_detail'),
    path('contact/new/', views.AddContactView.as_view(), name='contact_new'),
    path('contact/<int:pk>/edit/', views.ContactUpdateView.as_view(), name='contact_edit'),
]
