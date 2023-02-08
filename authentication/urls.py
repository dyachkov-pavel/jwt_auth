from django.urls import path
from .views import LoginView, RefreshTokenView

urlpatterns = [
    path('api/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]
