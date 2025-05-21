from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.shortcuts import redirect

from repair.views import (
    register_view,
    send_request_view,
    my_requests_view,
    admin_panel_view,
)

# 👇 наша функция выхода
def logout_view(request):
    logout(request)
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('send/', send_request_view, name='send'),
    path('my_requests/', my_requests_view, name='my_requests'),
    path('admin_panel/', admin_panel_view, name='admin_panel'),
]
