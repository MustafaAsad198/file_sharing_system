from django.urls import path, include
from .views import ops_login, ops_upload, client_signup, client_verify_email, client_login,index,ops_signup,client_home,ops_logout,download_files,client_logout

urlpatterns = [
    path("", index, name="home"),
    path('ops-login/', ops_login, name='ops_login'),
    path('ops-upload/<str:pk>', ops_upload, name='ops-upload'),
    path('client-signup/', client_signup, name='client_signup'),
    path('ops-signup/', ops_signup, name='ops_signup'),
    path('verify-email/<str:pk>', client_verify_email, name='client_verify_email'),
    path('client-home/<str:pk>', client_home, name='client_home'),
    path('client-login/', client_login, name='client_login'),
    path('ops-logout/<str:pk>', ops_logout, name='ops-logout'),
    path('client-logout/<str:pk>', client_logout, name='client-logout'),
    path('download-file/<str:pk>', download_files, name='downloaded_file'),
]
