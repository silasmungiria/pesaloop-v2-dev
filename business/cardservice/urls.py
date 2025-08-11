# urls.py
from django.urls import path
from cardservice.views import LinkCardView, ProcessPaymentView

urlpatterns = [
    path('cards/link/', LinkCardView.as_view()),
    path('cards/process-payment/', ProcessPaymentView.as_view()),
]