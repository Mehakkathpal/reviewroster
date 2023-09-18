from django.urls import path
from premiumfeature import views

urlpatterns = [
    path("company/",views.companyAPIView.as_view()),
]

