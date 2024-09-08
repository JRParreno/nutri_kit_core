from django.urls import path
from django.contrib.auth import views as auth_views

from user_profile.views import (ProfileView,
                                RegisterView, ChangePasswordView, 
                                UploadPhotoView, RequestPasswordResetEmail
                                )
from trivia.views import (QuestionListView,)
from deficiency.views import (DeficiencyListView, DeficiencyDetailView, DeficiencyFavoriteCreateView, DeficiencyFavoriteDeleteView,
                              DeficiencyFavoriteListView)
from treatment.views import (RemedyListView, RemedyDetailView, RemedyFavoriteCreateView, RemedyFavoriteDeleteView,
                             RemedyFavoriteListView)
from food.views import (FoodListView, FoodDetailView, VitaminListView, VitaminDetailView, FoodFavoriteCreateView, FoodFavoriteDeleteView,
                        VitaminFavoriteCreateView, VitaminFavoriteDeleteView, FoodFavoriteListView, VitaminFavoriteListView
                        )
from meal.views import (UserMealPlanRegisterView, UserMealPlanListView, UserMealPlanDetailView,
                        DayMealCompletionViewSet, UserMealPlanDeleteView
                        )

app_name = 'api'


urlpatterns = [
     path('signup', RegisterView.as_view(), name='signup'),
     path('profile', ProfileView.as_view(), name='profile'),
     path('upload-photo/<pk>', UploadPhotoView.as_view(), name='upload-photo'),
     path('change-password', ChangePasswordView.as_view(), name='change-password'),

     path('forgot-password', RequestPasswordResetEmail.as_view(),
          name='forgot-password '),
     path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
              template_name='password_reset_confirm.html'
              ),
         name='password-reset-confirm'),
     
     # Trivia
     path('trivia/list', QuestionListView.as_view(), name='trivia-list'),
     
     
     # Deficiency
     path('deficiency/list', DeficiencyListView.as_view(), name='deficiency-list'),
     path('deficiency/detail/<pk>', DeficiencyDetailView.as_view(), name='deficiency-detail'),
     path('deficiency-favorite/list/', DeficiencyFavoriteListView.as_view(), name='list_deficiency_favorite'),
     path('deficiency-favorite/create/', DeficiencyFavoriteCreateView.as_view(), name='create_deficiency_favorite'),
     path('deficiency-favorite/delete/<int:deficiency_id>/', DeficiencyFavoriteDeleteView.as_view(), name='delete_deficiency_favorite'),

     # Remedy/Treatment
     path('remedy/list', RemedyListView.as_view(), name='remedy-list'),     
     path('remedy/detail/<pk>', RemedyDetailView.as_view(), name='remedy-detail'),   
     path('remedy-favorite/list/', RemedyFavoriteListView.as_view(), name='list_remedy_favorite'), 
     path('remedy-favorite/create/', RemedyFavoriteCreateView.as_view(), name='create_remedy_favorite'),
     path('remedy-favorite/delete/<int:remedy_id>/', RemedyFavoriteDeleteView.as_view(), name='delete_remedy_favorite'),
     
     
     # Food
     path('food/list', FoodListView.as_view(), name='food-list'),     
     path('food/detail/<pk>', FoodDetailView.as_view(), name='food-detail'),     
     path('food-favorite/list/', FoodFavoriteListView.as_view(), name='list_food_favorite'), 
     path('food-favorite/create/', FoodFavoriteCreateView.as_view(), name='create_food_favorite'),
     path('food-favorite/delete/<int:food_id>/', FoodFavoriteDeleteView.as_view(), name='delete_food_favorite'),
     
     # Vitamin
     path('vitamin/list', VitaminListView.as_view(), name='vitamin-list'),     
     path('vitamin/detail/<pk>', VitaminDetailView.as_view(), name='vitamin-detail'),     
     path('vitamin-favorite/list/', VitaminFavoriteListView.as_view(), name='list_vitamin_favorite'), 
     path('vitamin-favorite/create/', VitaminFavoriteCreateView.as_view(), name='create_vitamin_favorite'),
     path('vitamin-favorite/delete/<int:vitamin_id>/', VitaminFavoriteDeleteView.as_view(), name='delete_vitamin_favorite'),
     
     # Meal
     path('meal/plan/child/register', UserMealPlanRegisterView.as_view(), name='meal-plan-register'),     
     path('meal/plan/child/list', UserMealPlanListView.as_view(), name='meal-plans'),     
     path('meal/plan/child/detail/<int:usermealplan_id>/meal-plan/<int:mealplan_id>/', UserMealPlanDetailView.as_view(), name='meal-plan-detail'),     
     path('meal/plan/child/complete/<pk>', DayMealCompletionViewSet.as_view({'patch': 'partial_update'}), name='meal-plan-complete'),     
     path('meal/plan/child/delete/<pk>', UserMealPlanDeleteView.as_view(), name='meal-plan-delete'),     

]
