from django.urls import path
from feemanagement import views

urlpatterns = [
    path("feestatus/",views.feestatusAPIView.as_view())
]

