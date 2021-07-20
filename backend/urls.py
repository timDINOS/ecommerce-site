from django.urls import path
from .views import (
    CheckoutDesign
)

app_name = 'core'

urlpatterns = [
    path('checkout/', CheckoutDesign.as_view(), name='checkout')
    
]