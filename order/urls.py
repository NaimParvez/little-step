from django.urls import path


from .views import (
    Checkout,
)



urlpatterns = [
    path('checkout/',Checkout.as_view(),name='checkout'),
    path('order/',Checkout.as_view(),name='order'),
]
