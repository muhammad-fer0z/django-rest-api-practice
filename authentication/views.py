from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, views
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.urls import reverse
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, \
    PasswordResetPasswordSerializer, SetNewPasswordApiSerializer
from .models import User
from .utils import Util
from .renderers import UserRenderers


# Create your views here.
class LoginApiView(GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderers,)

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        user = request.data
        register_serializer = self.serializer_class(data=user)
        register_serializer.is_valid(raise_exception=True)
        register_serializer.save()
        user_data = register_serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        Util.email_data(request, token, user, reverse('email-verify'))

        return Response(user_data, status=status.HTTP_201_CREATED)


class VarifyEmail(views.APIView):
    email_verification_serializer = EmailVerificationSerializer
    token_params_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description',
                                            type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_params_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Email Successfully Activated!'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation token expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetPasswordApiView(GenericAPIView):
    serializer_class = PasswordResetPasswordSerializer

    def post(self, request):
        data = {'request': request, 'data': request.data}
        serializer = self.serializer_class(data=data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uuid64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            Util.email_data_serializer(request, token, user,
                                       reverse('password-reset-token', kwargs={'uuid64': uuid64, 'token': token}))

            return Response({'success': 'We have sent you a link for reset password.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email not found. First register your self.'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordTokenCheckApiView(GenericAPIView):
    serializer_class = PasswordResetPasswordSerializer

    def get(self, request, uuid64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uuid64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please a new one.'})
            return Response({'success': True, 'message': 'Credentials valid.', 'uuid64': uuid64},
                            status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({'error': 'Token is not valid, please a new one.'})


class SetNewPasswordApiView(GenericAPIView):
    serializer_class = SetNewPasswordApiSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset successfully', }, status=status.HTTP_200_OK)
