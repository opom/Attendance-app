from django.urls import path
from. import views

urlpatterns= [
   # path('',views.home),
    path('registration/',views.signupform),
    path('signup/',views.Signup,name='signup'),
    path('',views.User_login,name='login'),
    path('profile/',views.user_profile,name='profile'),
    path('logout/',views.logout_view,name='logout'),
    path('timestamp/',views.timestamp,name='timestamp'),
    path('emp_detail/',views.employee_detail,name='emp_detail'),
    path('detail/',views.detail,name='detail'),
    path('changepassword/',views.change_password,name='changepassword'),
]