from rest_framework import generics, permissions, response, status
from rest_framework.exceptions import NotFound

from core.calc_birthdate import calculate_age
from .models import HealthStatus, UserMealPlan, MealPlan
from .serializers import (UserMealPlanRegisterSerializer, 
                          UserListMealPlanSerializer,
                          MealPlanSerializer)
from datetime import datetime, date


class UserMealPlanRegisterView(generics.CreateAPIView):
    serializer_class = UserMealPlanRegisterSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        name = request.data.get('name')
        birthdate_str = request.data.get('birthdate')
        height = request.data.get('height')
        weight = request.data.get('weight')
        health_status = request.data.get('health_status').lower()
        gender = request.data.get('gender')
        health_status_response = HealthStatus.objects.filter(status=health_status)
        
        if not health_status_response.exists():
            return response.Response({'error_message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        birthdate = datetime.strptime(birthdate_str, "%m/%d/%Y")
        age =calculate_age(birthdate)
        
        meal_plans = MealPlan.objects.filter(age=age)
        
        if not meal_plans.exists():
        #    raise serializers.ValidationError(errors)
            return response.Response({'error_message': 'Age is not applicable.'}, status=status.HTTP_400_BAD_REQUEST)



        
        user_meal_plan = UserMealPlan.objects.create(user=self.request.user, meal_plan=meal_plans.first(), name=name,
                                                     gender=gender,
                                    birthdate=birthdate, height=height, weight=weight, health_status=health_status_response.first()
                                    )
        
        return response.Response(
            {
                'usermealplan_id': str(user_meal_plan.pk),
                'mealplan_id': str(meal_plans.first().pk)
            },
            status=status.HTTP_200_OK
        )


class UserMealPlanListView(generics.ListAPIView):
    serializer_class = UserListMealPlanSerializer
    queryset = UserMealPlan.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class UserMealPlanDetailView(generics.RetrieveAPIView):
    serializer_class = MealPlanSerializer
    queryset = MealPlan.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    
    def get_object(self):
        # Extract parameters from the URL
        usermealplan_id = self.kwargs.get('usermealplan_id')
        mealplan_id = self.kwargs.get('mealplan_id')

        # Retrieve the UserMealPlan instance based on usermealplan_id
        try:
            user_meal_plan = UserMealPlan.objects.get(pk=usermealplan_id)
        except UserMealPlan.DoesNotExist:
            raise NotFound(detail="UserMealPlan not found")

        # Additional checks or logic can be applied here using mealplan_id if needed

        return user_meal_plan
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['mealplan_id'] = self.kwargs.get('mealplan_id')
        context['usermealplan_id'] = self.kwargs.get('usermealplan_id')

        return context