from django.urls import path
from. import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns= [
    path('registration/',views.signupform),
    path('signup/',views.Signup,name='signup'),
    path('',views.User_login,name='login'),
    path('profile/',views.user_profile,name='profile'),
    path('logout/',views.logout_view,name='logout'),
    #path('timestamp/',views.timestamp,name='timestamp'),
    path('emp_detail/',views.employee_detail,name='emp_detail'),
    path('detail/',views.detail,name='detail'),
    path('download/',views.download,name='download'),
    path('changepassword/',views.change_password,name='changepassword'),
    path("password_reset/", views.password_reset_request, name="password_reset")

]