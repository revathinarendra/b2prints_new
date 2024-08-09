from django.urls import path
from .views import OrderCreateView,order_success

urlpatterns = [
    path('order_here/', OrderCreateView.as_view(), name='order_here'),
    path('order_success/<str:order_id>/',order_success,name='order_success')
] 

