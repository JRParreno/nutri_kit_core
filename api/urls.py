from django.urls import path
from django.contrib.auth import views as auth_views

from user_profile.views import (ProfileView,
                                RegisterView, ChangePasswordView, 
                                UploadPhotoView, RequestPasswordResetEmail
                                )
from trivia.views import (QuestionListView,)
from deficiency.views import (DeficiencyListView, DeficiencyDetailView)
from treatment.views import (RemedyListView, RemedyDetailView)
from food.views import (FoodListView, FoodDetailView, VitaminListView, VitaminDetailView)

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
     path('deficiency/detail/<pk>', DeficiencyDetailView.as_view(), name='deficiency-detail'),


     # Remedy/Treatment
     path('remedy/list', RemedyListView.as_view(), name='remedy-list'),     
     path('remedy/detail/<pk>', RemedyDetailView.as_view(), name='remedy-detail'),    
      
     # Food
     path('food/list', FoodListView.as_view(), name='food-list'),     
     path('food/detail/<pk>', FoodDetailView.as_view(), name='food-detail'),     
     
     # Vitamin
     path('vitamin/list', VitaminListView.as_view(), name='vitamin-list'),     
     path('vitamin/detail/<pk>', VitaminDetailView.as_view(), name='vitamin-detail'),     
]
