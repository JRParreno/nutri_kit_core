from datetime import datetime
import os
import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import get_access_token_model
from oauth2_provider.signals import app_authorized
from oauth2_provider.views.base import TokenView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from meal.excel_reader import read_excel_file
from meal.health_status_formula import getHealthForZHA, getHealthForZWA, getHealthForZWH, select_formula 


class TokenViewWithUserId(TokenView):
    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_token_response(request)

        if status == 200:
            body = json.loads(body)
            access_token = body.get("access_token")
            if access_token is not None:
                try:
                    token = get_access_token_model().objects.get(
                        token=access_token)
                    
                    # Check if the user has a profile
                    profile = token.user.profile
                    if profile is None:
                        raise ObjectDoesNotExist("User profile does not exist")

                    app_authorized.send(
                        sender=self, request=request,
                        token=token)
                    
                    # Add user ID to the response body
                    data = {
                        "pk": str(token.user.pk),
                        "profilePk": str(profile.pk),
                        "username": token.user.username,
                        "firstName": token.user.first_name,
                        "lastName": token.user.last_name,
                        "email": token.user.email,
                        "age": profile.age,
                        "profilePhoto": request.build_absolute_uri(profile.profile_photo.url) if profile.profile_photo else None,
                        "access_token": access_token,
                        "refresh_token": body.get("refresh_token")
                    }
                    body = json.dumps(data)
                    
                except ObjectDoesNotExist:
                    # Handle case where user profile doesn't exist
                    return JsonResponse({'error_description': 'User profile does not exist'}, status=400)
   
        response = HttpResponse(content=body, status=status)
        for k, v in headers.items():
            response[k] = v
        return response
    



def display_excel_data(request):
    birthdate_str = '09/21/2020'
    birthdate = datetime.strptime(birthdate_str, "%m/%d/%Y")

    zhw = getHealthForZWH(89.5, 11.2, 3, 'Male')
    zha = getHealthForZHA(89.5, birthdate, 'Male')
    zwa =  getHealthForZWA(11.2, birthdate, 'Male')
    
    print(f"ZHW: {zhw}")
    print(f"ZHA: {zha}")
    print(f"ZWA: {zwa}")
    
    formulas = {
        'formula_one': zhw,
        'formula_two': zha,
        'formula_three': zwa
    }
    
    formula = select_formula(formulas)
    print(formula)
    
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
    
    print(json.dumps(health_status_infos))


    # Pass the data to the template
    return render(request, 'display_excel.html')