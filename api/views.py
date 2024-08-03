from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializer import UserLoginSerializer, UserRegisterSerializer, EmailVerificationSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from api.serializer import DailyCheckinSerializer
from api.models import DailyCheckin

User = get_user_model()

# Create your views here.


class UserRegistrationAPI(APIView):
    def get(self, request):
        return Response({"message": "register!"}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'registeration successfull!', 'data': serializer.data}, status=status.HTTP_201_CREATED)

        return Response({"serializer.data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPI(APIView):
    def get(self, request):
        return Response({"message": "login!"}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            serializer.save()
            return Response({'message': 'login successfull!'}, serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response({"serializer.data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerifyAPI(APIView):
    def get(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():

            subject = 'Account Verification Email'
            otp = random.randint(0000, 9999)
            message = 'OTP: ' + str(otp)
            email_to = serializer.validated_data['email']
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [email_to])

            user = User.objects.get(email=email_to)
            user.otp = otp
            user.save()

            return Response({"message": "verification email sent!"}, status=status.HTTP_200_OK)
        return Response({"serializer.data": serializer.errors}, status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            user = User.objects.get(email=email)
            if user.otp == otp:
                user.is_active = True
                user.save()
                return Response({"message": 'Email Verified'}, status=status.HTTP_202_ACCEPTED)
            return Response({"message": 'Invalid OTP'}, status=status.HTTP_202_ACCEPTED)
        return Response({"serializer.data": serializer.errors}, status=status.HTTP_202_ACCEPTED)


class PasswordResetAPI(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                reset_link = f"http://127.0.0.1:8000/api/reset-password?token={token}&email={email}"
                send_mail(
                    'Password Reset Request',
                    f'Click the link to reset your password: {reset_link}',
                    'ramshasuhail46@gmail.com',
                    [email],
                )
                return Response({"message": "Password reset link sent!"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPI(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(email=email)
                if default_token_generator.check_token(user, token):
                    user.set_password(new_password)
                    user.save()
                    return Response({"message": "Password has been reset!"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DailyCheckinAPI(APIView):
    def post(self, request):
        serializer = DailyCheckinSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'email': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            datetime_of_checkin = serializer.validated_data['datetime_of_checkin']
            DailyCheckin.objects.create(
                user=user, datetime_of_checkin=datetime_of_checkin)
            return Response({'message': 'check-in time added', 'data': serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
