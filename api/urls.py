from django.urls import path
from django.contrib.auth import views as auth_views

from user_profile.views import (ProfileView,
                                RegisterView, ChangePasswordView, 
                                UploadPhotoView, RequestPasswordResetEmail
                                )
from trivia.views import (QuestionListView,)
from deficiency.views import (DeficiencyListView)

app_name = 'api'


urlpatterns = [
     path('signup', RegisterView.as_view(), name='signup'),
     path('profile', ProfileView.as_view(), name='profile'),
     path('upload-photo/<pk>', UploadPhotoView.as_view(), name='upload-photo'),
     path('change-password', ChangePasswordView.as_view(), name='change-password'),

     path('forgot-password', RequestPasswordResetEmail.as_view(),
          name='forgot-password '),
     path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),
     
     # Trivia
     path('trivia/list', QuestionListView.as_view(), name='trivia-list'),
     
     
     # Deficiency
     path('deficiency/list', DeficiencyListView.as_view(), name='deficiency-list'),
     
]
