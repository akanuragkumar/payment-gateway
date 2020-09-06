from django.urls import path

from .views import *

urlpatterns = [
    path('payment-method', PaymentMethodListCreateView.as_view(), name='payment-method-list'),
    path('payment-detail', PaymentDetailListCreateView.as_view(), name='payment-detail-list')
]
