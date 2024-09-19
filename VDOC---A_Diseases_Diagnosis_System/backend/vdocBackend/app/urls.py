from django.urls import path
from . import views
# from .views import DiseaseList,DescriptionList,PrecautionList,MedicationList,DietList
# from .views import signup_view  , login_view ,get_csrf_token_view

urlpatterns = [
    path('disease/',views.DiseaseList.as_view()),
    path('description/',views.DescriptionList.as_view()),
    path('precaution/',views.PrecautionList.as_view()),
    path('medication/',views.MedicationList.as_view()),
    path('diet/',views.DietList.as_view()),
    # path('signup/',signuppage,name='signup'),
    # path('signup/', signup_view, name='signup'),
    # path('login/',logininpage,name='login'),
    # path('logout/',logoutpage,name='logout'),
    # path('csrf-token/', get_csrf_token_view, name='get_csrf_token'),  # CSRF Token endpoint

]


# # urls.py

# from django.urls import path
# from .views import signup_view, login_view, get_csrf_token_view

# urlpatterns = [
#     path('login/', login_view, name='login'),
#     path('csrf-token/', get_csrf_token_view, name='get_csrf_token'),
# ]


# from django.urls import path
# from .views import csrf_token_view, login_view,signup_view

# urlpatterns = [
#     path('signup/', signup_view, name='signup'),
#     path('csrf-token/', csrf_token_view, name='csrf_token'),
#     path('login/', login_view, name='login'),
# ]
