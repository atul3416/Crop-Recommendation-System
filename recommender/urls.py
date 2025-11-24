from django.urls import path

from .views import *

# app_name = 'recommender'

urlpatterns = [
    path('',home,name="home_page"),
    path('signup/',SignUp,name="sign_up"),
    path('predict/',PredictView,name="predict"),
    path('logout/',LogoutView,name="logout"),
    path('login/',LoginView,name="login"),
    path('user_history/',UserHistoryView,name="user_history"),
    path('history_delete/<int:id>/',UserHistoryDelete,name="user_delete_pred"),
    path('user_profile/',UserPro, name="user_profile"),
    path('change_pass/',ChangePassword,name="change_pass")
]