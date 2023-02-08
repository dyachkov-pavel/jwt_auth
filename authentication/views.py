import jwt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import permissions, status, views
from rest_framework.response import Response

from .serializers import LoginSerializer, RefreshTokenSerializer
from .tokens import (decode_token, generate_access_token,
                     generate_refresh_token, verify_token)

User = get_user_model()


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                access_token = generate_access_token(user)
                refresh_token = generate_refresh_token(user)
                user.set_refresh_token(refresh_token)
                user.refresh_token_count += 1
                user.save()
                return Response({'access_token': access_token,
                                 'refresh_token': refresh_token})
            return Response({'error': 'Invalid login credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)


class RefreshTokenView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            refresh_token = serializer.validated_data['refresh_token']
            try:
                is_valid, user_id = verify_token(refresh_token)
                if not is_valid:
                    return Response({'error': 'Refresh token is invalid or expired'},
                                    status=status.HTTP_401_UNAUTHORIZED)
            except jwt.exceptions.DecodeError:
                return Response({'error': 'Invalid refresh token'},
                                status=status.HTTP_401_UNAUTHORIZED)
            try:
                user = User.objects.get(id=user_id)
                payload = decode_token(refresh_token)
                if user.refresh_token_count != payload['token_count']:
                    return Response({'error': 'Refresh token has changed'},
                                    status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({'error': 'user does not exist'},
                                status=status.HTTP_400_BAD_REQUEST)

            access_token = generate_access_token(user)
            return Response({'access_token': access_token})
