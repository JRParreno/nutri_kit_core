from user_profile.email import Util
from user_profile.models import UserProfile
from rest_framework import generics, permissions, response, status
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.response import Response
import re
from oauth2_provider.models import (
    Application,
    RefreshToken,
    AccessToken
)
from datetime import (
    datetime,
    timedelta
)
from django.utils.crypto import get_random_string
from django.conf import settings
from user_profile.models import UserProfile
from .serializers import (ChangePasswordSerializer, ProfileSerializer, RegisterSerializer,
                          UploadPhotoSerializer, ResetPasswordEmailRequestSerializer)
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.template.loader import get_template
class RegisterView(generics.CreateAPIView):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create_access_token(self, user):
        application = Application.objects.all()

        if application.exists():
            self.expire_seconds = settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS']
            scopes = settings.OAUTH2_PROVIDER['SCOPES']
            expires = datetime.now() + timedelta(seconds=self.expire_seconds)
            token = get_random_string(32)
            refresh_token = get_random_string(32)

            access_token = AccessToken.objects.create(
                user=user,
                expires=expires,
                scope=scopes,
                token=token,
                application=application.first(),
            )

            refresh_token = RefreshToken.objects.create(
                user=user,
                access_token=access_token,
                token=refresh_token,
                application=application.first(),
            )

            return access_token, refresh_token

        return None

    def post(self, request, *args, **kwargs):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        age = request.data.get('age')
        email = request.data.get('email') 
        
        if User.objects.filter(email=email).exists():
            data = {
                "error_message": "Email already exists"
            }
            return response.Response(
                data=data,
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=email).exists():
            data = {
                "error_message": "Mobile number already exists"
            }
            return response.Response(
                data=data,
                status=status.HTTP_400_BAD_REQUEST
            )

        if password != confirm_password:
            data = {
                "error_message": "Password does not match"
            }
            return response.Response(
                data=data,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create(
            username=email, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        user_profile = UserProfile.objects.create(user=user, age=age)

        oauth_token, refresh_token = self.create_access_token(
            user)
        
        data = {
                "pk": str(user.pk),
                "profilePk": str(user_profile.pk),
                "username": user.username,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email,
                "age": user_profile.age,
                "profilePhoto": request.build_absolute_uri(user_profile.profile_photo.url) if user_profile.profile_photo else None,
                "access_token": oauth_token.token,
                "refresh_token": refresh_token.token
            }

        return response.Response(
            data=data,
            status=status.HTTP_200_OK
        )
        

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_profiles = UserProfile.objects.filter(user=user)

        if user_profiles.exists():
            user_profile = user_profiles.first()

            data = {
                "pk": str(user.pk),
                "profilePk": str(user_profile.pk),
                "username": user.username,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email,
                "age": user_profile.age,
                "profilePhoto": request.build_absolute_uri(user_profile.profile_photo.url) if user_profile.profile_photo else None,
            }

            return response.Response(data, status=status.HTTP_200_OK)

        else:
            error = {
                "error_message": "Please setup your profile"
            }
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        user_details = self.request.data.get('user')
        age = self.request.data.get('age')
        user_email = UserProfile.objects.filter(
            user__email=user_details['email']).exclude(user=user).exists()

        if user_email:
            error = {
                "error_message": "Email already exists"
            }
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

        user_profile = UserProfile.objects.get(user=user)

        user.email = user_details['email']
        user.first_name = user_details['first_name']
        user.last_name = user_details['last_name']
        user.username = user_details['email']
        user.save()

        user_profile.age = age
        user_profile.save()

        data = {
            "pk": str(user.pk),
            "profilePk": str(user_profile.pk),
            "username": user.username,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "email": user.email,
            "age": user_profile.age
        }
        return response.Response(data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request
        })
        return context

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"error_message": "Wrong old password."}, status=status.HTTP_400_BAD_REQUEST)
            new_password_entry = serializer.data.get("new_password")
            reg = "[^\w\d]*(([0-9]+.*[A-Za-z]+.*)|[A-Za-z]+.*([0-9]+.*))"
            pat = re.compile(reg)

            if 8 <= len(new_password_entry) <= 16:
                password_validation = re.search(pat, new_password_entry)
                if password_validation:
                    self.object.set_password(
                        serializer.data.get("new_password"))
                else:
                    return Response({"error_message":
                                     "Password must contain a combination of letters and numbers"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error_message":
                                 "Password must contain at least 8 to 16 characters"},
                                status=status.HTTP_400_BAD_REQUEST)

            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadPhotoView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UploadPhotoSerializer
    queryset = UserProfile.objects.all()


class RequestPasswordResetEmail(generics.CreateAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = []

    def post(self, request):
        email_address = request.data.get('email_address', '')
        check_identity = User.objects.filter(email__exact=email_address)
        if check_identity.exists():
            identity = check_identity.first()
            uidb64 = urlsafe_base64_encode(smart_bytes(identity.id))
            token = PasswordResetTokenGenerator().make_token(identity)

            relative_link = reverse(
                'api:password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            current_site = get_current_site(
                request=request).domain
            abs_url: str = f"https://{current_site}{relative_link}"

            context_email = {
                "url": abs_url,
                "full_name": f"{identity.first_name} {identity.last_name}"
            }
            message = get_template(
                'forgot_password/index.html').render(context_email)

            context = {
                'email_body': message,
                'to_email': identity.email,
                'email_subject': 'Reset your password'
            }

            Util.send_email(context)
        else:
            return response.Response({'error_message': 'Email not found!'}, status=status.HTTP_404_NOT_FOUND)

        return response.Response(
            {'success': 'We have sent you a link to reset your password'},
            status=status.HTTP_200_OK
        )