# /apps/users/serializers.py

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    사용자 정보 조회를 위한 Serializer
    """
    class Meta:
        model = User
        fields = ['user_id', 'kakao_id', 'nickname', 'profile_image', 'created_at']


class SocialLoginResponseSerializer(serializers.Serializer):
    """
    소셜 로그인 성공 시 응답을 위한 Serializer
    - access/refresh JWT 토큰과 사용자 정보를 함께 담아 보내버리기
    """
    access = serializers.CharField(help_text="JWT Access Token")
    refresh = serializers.CharField(help_text="JWT Refresh Token")
    user = UserSerializer(help_text="로그인한 사용자 정보")