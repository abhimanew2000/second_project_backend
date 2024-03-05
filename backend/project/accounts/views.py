from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from accounts.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserChangePasswordSerializer,
    SendPasswordResetEmailSerializer,
    UserPassworddResetSerializer,
    ChatsMessageSerializer,
)
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth import authenticate
from accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.views import LogoutView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from django.contrib.auth import logout
from .serializers import GoogleLoginSerializer
from django.contrib.auth import authenticate, login
from accounts.models import User, Chats
from django.contrib.auth import get_user_model

from rest_framework.generics import ListAPIView
from rest_framework import generics

from django.db.models import Subquery, OuterRef, Q
from .models import Profile


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    permission_classes=[AllowAny]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "msg": "Registration successfull"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user_with_google(request):
    if "google_oauth" in request.data:
        google_data = request.data["google_oauth"]

        serializer = UserRegistrationSerializer(
            data={
                "email": google_data.get("email"),
                "name": google_data.get("name"),
                "tc": True,
                "password": "some_random_password",
                "password2": "some_random_password",
            }
        )

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response({"msg": "Registration successful"})
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=400)

    return Response({"msg": "Invalid request data"}, status=400)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            if user:
                token = get_tokens_for_user(user)
                return Response(
                    {
                        "token": token,
                        "msg": "Login Success",
                        "user_name": user.name,
                        "email": user.email,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "errors": {
                            "non_field_errors": ["Email or password is not Correct"]
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )


@api_view(["POST"])
@permission_classes([AllowAny])
def google_login(request):
    print("enterrrred")
    try:
        google_data = request.data.get("google_oauth")
        print(google_data, "doodle")

        user = User.objects.filter(email=google_data.get("email")).first()
        print(user, "userrrrrrrr")

        if user:
            serializer = UserLoginSerializer(
                data={
                    "email": google_data.get("email"),
                    "password": "some_random_password",
                }
            )
            serializer.is_valid(raise_exception=True)
            user = authenticate(
                email=google_data.get("email"), password="some_random_password"
            )
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response(
                {
                    "token": {"access": access_token},
                    "msg": "Login Success",
                    "user_name": user.name,
                    "email": user.email,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"msg": "User not registered"}, status=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        return Response(
            {"msg": "Error during Google login", "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        logout(request)

        return Response({"msg": "Logout successful"}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "password Changed Successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "password reset link send.Please check your Email"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request, uid, token, format=None):
        serializer = UserPassworddResetSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "password Reset Successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyInbox(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ChatsMessageSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]

        messages = Chats.objects.filter(
            id__in=Subquery(
                User.objects.filter(
                    Q(sender__receiver=user_id) | Q(receiver__sender=user_id)
                )
                .distinct()
                .annotate(
                    last_msg=Subquery(
                        Chats.objects.filter(
                            Q(sender=OuterRef("id"), receiver=user_id)
                            | Q(receiver=OuterRef("id"), sender=user_id)
                        )
                        .order_by("-id")[:1]
                        .values_list("id", flat=True)
                    )
                )
                .values_list("last_msg", flat=True)
                .order_by("-id")
            )
        ).order_by("-id")

        return messages


class GetMessages(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ChatsMessageSerializer

    def get_queryset(self):
        sender_id = self.kwargs["sender_id"]
        receiver_id = self.kwargs["receiver_id"]

        messages = Chats.objects.filter(
            sender__in=[sender_id, receiver_id], receiver__in=[sender_id, receiver_id]
        )
        return messages


class SendMessage(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ChatsMessageSerializer


class ProfileDetail(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserProfileSerializer
    queryser = Profile.objects.all()


class SearchUser(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        users = Profile.objects.filter(
            Q(user__name__icontains=username)
            | Q(full_name__icontains=username)
            | Q(user__email__icontains=username)
        )

        if not users.exists():
            return Response(
                {"details": "No Users Found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
