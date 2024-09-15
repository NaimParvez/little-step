from django.urls import path


from .views import (
    Checkout,
)



urlpatterns = [
    path('checkout/',Checkout.as_view(),name='checkout'),
]
