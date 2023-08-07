from django.urls import path
from playground import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('verifyemail', views.verify_email, name='verifyemail'),
    path('validatecode/', views.validate_code, name='validate_code'),
    path('getinvite/', views.get_invite, name='get_invite')
]