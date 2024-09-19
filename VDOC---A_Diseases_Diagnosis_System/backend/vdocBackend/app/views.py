from django.shortcuts import render , redirect
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
# from django.contrib.auth.models import User
# from django.contrib.auth import login , logout , authenticate
# from django.db import IntegrityError
from .serializers import *
from .models import *
from rest_framework.generics import ListAPIView


class DiseaseList(ListAPIView) :
    queryset = Diseases.objects.all()
    serializer_class = DiseaseSerializer

class DescriptionList(ListAPIView) :
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer

class PrecautionList(ListAPIView) :
    queryset = Precaution.objects.all()
    serializer_class = PrecautionSerializer

class MedicationList(ListAPIView) :
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer

class DietList(ListAPIView) :
    queryset = Diet.objects.all()
    serializer_class = DietSerializer

# # # Create your views here.

# # def signuppage(request) :
# #     print('here')
# #     if request.method == 'POST':
# #         print('inside')
# #         data = json.loads(request.body)
# #         username = data.get('email')
# #         password = data.get('password')
# #         print(data)

# #         # user = authenticate(request, username=username, password=password)
        
# #         if username is not None:
# #             # Create session or generate a token for the user
# #             return JsonResponse({'message': 'Login successful'})
# #         else:
# #             return JsonResponse({'error': 'Invalid credentials'}, status=400)
# #     # if request.method == 'GET' :
# #         # return render(request,'signuppage.html',{'form':UserCreationForm})
# #         # return HttpResponse('false')
# #     # else :
# #         # print(request.POST['email']+"     "+request.POST['password'])
# #         # return HttpResponse(f"<h1>Email : {request.POST['email']} , Password : {request.POST['password']}</h1>")
# #         # if request.POST['password1'] == request.POST['password2'] :
# #         #     try :
# #         #         user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
# #         #         user.save()
# #         #         login(request,user)
# #         #         return redirect('home')
# #         #     except IntegrityError :
# #         #         return render(request,'signuppage.html',{'error':'Username already exists','form':UserCreationForm})
# #         # else :
# #         #     return render(request,'signuppage.html',{'form':UserCreationForm,'error':'passwords do not match'})


# # views.py

# from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
# import json
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login
from django.db import IntegrityError

# @ensure_csrf_cookie
# def get_csrf_token_view(request):
#     """
#     A view to ensure that the CSRF token is set in the client's cookies.
#     """
#     return JsonResponse({'message': 'CSRF token set'}, status=200)


# @csrf_protect
# def login_view(request):
#     """
#     Handles user login by authenticating the user.
#     Requires a valid CSRF token.
#     """
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             username = data.get('username')
#             password = data.get('password')

#             if not username or not password:
#                 return JsonResponse({'error': 'Missing required fields'}, status=400)

#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return JsonResponse({'message': 'Login successful!'}, status=200)
#             else:
#                 return JsonResponse({'error': 'Invalid username or password'}, status=400)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
#     else:
#         return JsonResponse({'error': 'Only POST method is allowed'}, status=405)



# from django.http import JsonResponse
# from django.middleware.csrf import get_token
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.csrf import ensure_csrf_cookie
# import json
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User

# @ensure_csrf_cookie
# def csrf_token_view(request):
#     return JsonResponse({'csrfToken': get_token(request)})

# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             username = data.get('username')
#             password = data.get('password')

#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return JsonResponse({'message': 'Login successful!'}, status=201)
#             else:
#                 return JsonResponse({'error': 'Invalid credentials'}, status=401)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
#     return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

# @csrf_exempt
# def signup_view(request):
#     """
#     Handles user signup by creating a new user.
#     Requires a valid CSRF token.
#     """
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             username = data.get('username')
#             email = data.get('email')
#             password = data.get('password')

#             if not username or not email or not password:
#                 return JsonResponse({'error': 'Missing required fields'}, status=400)

#             user = User.objects.create_user(username=username, email=email, password=password)
#             user.save()

#             return JsonResponse({'message': 'User created successfully!'}, status=201)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
#         except IntegrityError:
#             return JsonResponse({'error': 'Username already exists'}, status=400)
#     else:
#         return JsonResponse({'error': 'Only POST method is allowed'}, status=405)