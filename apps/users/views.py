# /apps/users/views.py

import os
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated # 권한 설정용

from .models import User
from .serializers import UserSerializer, SocialLoginResponseSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# 카카오 로그인 처리 파트
class KakaoLoginView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        auth_code = request.data.get('code')
        if not auth_code:
            return Response({"error": "인가 코드가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            # --- 💡 바로 이 부분입니다! ---
            # "KAKAO_REST_API_KEY" -> "KAKAO_API_KEY"로 수정하여 .env 파일과 일치시킵니다.
            "client_id": os.getenv("KAKAO_API_KEY"),
            "redirect_uri": os.getenv("KAKAO_REDIRECT_URI"),
            "code": auth_code,
        }
        
        # 카카오 서버로부터 토큰 발급 요청
        token_response = requests.post(kakao_token_api, data=data)
        
        token_json = token_response.json()
        
        if 'error' in token_json:
            print(f"카카오 토큰 발급 실패: {token_json}")
            return Response(token_json, status=status.HTTP_400_BAD_REQUEST)

        access_token = token_json.get("access_token")

        # 받은 카카오 토큰으로 다시 카카오 서버에 '사용자 정보'를 요청
        user_info_api = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = requests.get(user_info_api, headers=headers)
        user_info = user_info_response.json()
        kakao_id = user_info.get("id")
        if not kakao_id:
            return Response({"error": "카카오 사용자 정보 조회에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 받은 카카오 ID로 우리 DB에 사용자가 있는지 확인하고, 없으면 새로 만들기
        user, created = User.objects.get_or_create(
            kakao_id=kakao_id,
            defaults={
                'nickname': user_info.get("properties", {}).get("nickname"),
                'profile_image': user_info.get("properties", {}).get("profile_image"),
            }
        )
        
        # 우리 서비스 전용 JWT 토큰 (access, refresh)을 생성.
        token = TokenObtainPairSerializer.get_token(user)
        
        # 최종적으로 클라이언트에게 보낼 응답 만들기.
        response_data = {
            'access': str(token.access_token),
            'refresh': str(token),
            'user': user
        }
        serializer = SocialLoginResponseSerializer(instance=response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 닉네임 중복 확인 파트 (수정 없음)
class NicknameCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        nickname = request.query_params.get('nickname')
        if not nickname:
            return Response({"error": "닉네임을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        is_duplicate = User.objects.filter(nickname=nickname).exists()
        return Response({"is_available": not is_duplicate}, status=status.HTTP_200_OK)


# '내 정보' 조회 및 수정 파트 (수정 없음)
class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        new_nickname = request.data.get('nickname')
        if not new_nickname:
            return Response({"error": "새 닉네임을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(nickname=new_nickname).exclude(pk=request.user.pk).exists():
            return Response({"error": "이미 사용 중인 닉네임입니다."}, status=status.HTTP_409_CONFLICT)
            
        user = request.user
        user.nickname = new_nickname
        user.save()
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
