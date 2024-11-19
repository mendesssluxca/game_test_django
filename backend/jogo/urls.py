from django.urls import path
from .views import SubmitScoreAPIView

urlpatterns = [
    path('submit-score/', SubmitScoreAPIView.as_view(), name='submit-score'),
]
