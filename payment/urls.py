from django.urls import path
from . import views

urlpatterns = [
    path("create-checkout-session/<int:pk>", views.StripeCheckoutView.as_view(), name="test_payment"),
    path("webhook",views.stripe_webhook, name="webhook"),
    path("payment-details/<int:pk>/", views.PaymentDetailsListCreateEdit.as_view(), name="payment-details"),
    path("orders-history", views.OrderHistoryList.as_view(), name="orders-history"),
]

# stripe login
# stripe listen --forward-to localhost:8000/payment/webhook

sss