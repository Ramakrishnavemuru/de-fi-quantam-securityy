from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('wallet/create/', views.create_wallet_view, name='create_wallet'),
    path('security-preferences/', views.security_preferences_view, name='security_preferences'),
]

