from django.urls import path
from .views import (
    CheckoutDesign, PaymentView, RequestNewRefund, ApplyCoupon, ItemSummary, HomeDesign
)

app_name = 'core'

urlpatterns = [
    path('checkout/', CheckoutDesign.as_view(), name='checkout'),
    path('payment/<payment_option>/', PaymentView.as_view(), name="payment"),
    path('request-refund/', RequestNewRefund.as_view(), name="request-refund"),
    path('add-coupon/', ApplyCoupon.as_view(), name="add-coupon"),
    path('product/<slug>/', ItemSummary.as_view(), name="product"),
    path('', HomeDesign.as_view(), name='home')
]

