# /apps/users/urls.py

from django.urls import path
from .views import KakaoLoginView, NicknameCheckView, UserMeView

urlpatterns = [
    # 주소: /api/v1/auth/social/kakao/ -> KakaoLoginView
    path('auth/social/kakao/', KakaoLoginView.as_view(), name='kakao-login'),
    
    # 주소: /api/v1/users/check-nickname/ -> NicknameCheckView
    path('users/check-nickname/', NicknameCheckView.as_view(), name='check-nickname'),
    
    # 주소: /api/v1/users/me/ -> UserMeView
    path('users/me/', UserMeView.as_view(), name='me'),
]