from django.urls import path

from stripepayment import views
urlpatterns = [
     path('payment-intent/', views.create_payment_intent),
     path('save-stripe-info/',views.save_stripe_info),
     path('process-payment/',views.process_payment),
     path('subscription-status/',views.get_subscription_status),
     path('stripe-balance/',views.get_balance),
     path('session-checkout/',views.create_checkout_session),
     path('subscription_status/',views.subscriptionStatusView.as_view()),
     path('success_view/',views.success_view)
]


