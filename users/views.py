from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.db import IntegrityError
from django.contrib.auth import login, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from users.models import CustomUser


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        try:
            serializer.save()
            content = {
                "status": "success",
                "message": "User registered successfully",
                "user": serializer.data,
            }
            return Response(content, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response(
                {"status": "error", "error": "User with this email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"status": "error", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@permission_classes([AllowAny])
class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if email and password:
            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                serializer = UserSerializer(user)
                content = {
                    "status": "success",
                    "message": "Login successful",
                    "user": serializer.data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
                return Response(content, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"status": "error", "error": "Authentication failed"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                {"status": "error", "error": "Both email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserListView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class ProfileEdit(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
