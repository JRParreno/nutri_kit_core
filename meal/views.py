import json
from rest_framework import generics, permissions, response, status, viewsets
from rest_framework.exceptions import NotFound

from core.calc_birthdate import calculate_age
from meal.health_status_formula import getHealthForZHA, getHealthForZWA, getHealthForZWH, select_formula
from .models import UserMealPlan, MealPlan, DayMealCompletion
from .serializers import (UserMealPlanRegisterSerializer, 
                          UserListMealPlanSerializer,
                          MealPlanSerializer, DayMealCompletionSerializer, UserMealPlanSerializer)
from datetime import datetime, date


class UserMealPlanRegisterView(generics.CreateAPIView):
    serializer_class = UserMealPlanRegisterSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        name = request.data.get('name')
        birthdate_str = request.data.get('birthdate')
        height = float(request.data.get('height'))
        weight = float(request.data.get('weight'))
        gender = request.data.get('gender')
        
        
        birthdate = datetime.strptime(birthdate_str, "%m/%d/%Y")
        age = calculate_age(birthdate)
        
        zhw = getHealthForZWH(height, weight, age, gender)
        zha = getHealthForZHA(height, birthdate, gender)
        zwa =  getHealthForZWA(weight, birthdate, gender)
        
        """
            get the values less than equal to -2
            if the values hava all positive get the highest value and must be
            greater than equal to 2 if all the values are the same the priority 
            is stunted likewise obese
            
            take note: use formula 3 if all the values are positive
        """
        formulas = {
            'formula_one': zhw,
            'formula_two': zha,
            'formula_three': zwa
        }
        
        print(formulas)
    
        health_status_info = select_formula(formulas)
        
        health_status_infos = []
        
        if zhw < -2 or zhw < -3:
            health_status_infos.append('wasted')
        if zha < -2 or zha < -3:
            health_status_infos.append('stunted')
        if zwa < -2 or zwa < -3:
            health_status_infos.append('underweight')
        elif zwa > 2 and zwa <= 3:
            health_status_infos.append('overweight')
        elif zwa > 3:
            health_status_infos.append('obese')
        else:
            pass
        
        meal_plans = MealPlan.objects.filter(age=age)
        
        if not meal_plans.exists():
            return response.Response({'error_message': 'Age is not applicable.'}, status=status.HTTP_400_BAD_REQUEST)

        meal_plans = meal_plans.filter(health_status_info=health_status_info)

        if not meal_plans.exists():
            return response.Response({'error_message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

        if not health_status_info:
            return response.Response({'error_message': 'Child is healthy'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_meal_plan = UserMealPlan.objects.create(user=self.request.user, meal_plan=meal_plans.first(), name=name,
                                                     gender=gender, health_status_info=health_status_info,
                                    birthdate=birthdate, height=height, weight=weight
                                    )
        
        if len(health_status_infos) == 3:
            health_status_infos.pop()
        elif len(health_status_infos) == 2 and 'wasted' in health_status_infos and 'underweight' in health_status_infos:
             health_status_infos = ['wasted']
        else:
            pass
        
        return response.Response(
            {
                'usermealplan_id': str(user_meal_plan.pk),
                'mealplan_id': str(meal_plans.first().pk),
                'health_status_infos': health_status_infos,
            },
            status=status.HTTP_200_OK
        )


class UserMealPlanListView(generics.ListAPIView):
    serializer_class = UserListMealPlanSerializer
    queryset = UserMealPlan.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-created_at')


class UserMealPlanDetailView(generics.RetrieveAPIView):
    serializer_class = MealPlanSerializer
    queryset = MealPlan.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    
    def get_object(self):
        usermealplan_id = self.kwargs.get('usermealplan_id')
        try:
            user_meal_plan = UserMealPlan.objects.get(pk=usermealplan_id)
        except UserMealPlan.DoesNotExist:
            raise NotFound(detail="UserMealPlan not found")

        return user_meal_plan
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['mealplan_id'] = self.kwargs.get('mealplan_id')
        context['usermealplan_id'] = self.kwargs.get('usermealplan_id')

        return context


class UserMealPlanDeleteView(generics.DestroyAPIView):
    serializer_class = UserMealPlanSerializer
    queryset = UserMealPlan.objects.all()
    permission_classes = [permissions.IsAuthenticated,]



class DayMealCompletionViewSet(viewsets.ModelViewSet):
    queryset = DayMealCompletion.objects.all()
    serializer_class = DayMealCompletionSerializer
    permission_classes = (permissions.IsAuthenticated,)
