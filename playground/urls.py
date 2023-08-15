from django.urls import path
from playground import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('verifyemail', views.verify_email, name='verifyemail'),
    path('verifyemail/<int:validation_id>/', views.validate_code, name='validate_code'),
    #path('validatecode/', views.validate_code, name='validate_code'),
    path('getinvite/<int:person_key>/', views.get_invite, name='get_invite'),
    path('showinvite/<int:invitee_key>/<int:invitation_key>/', views.show_invite, name='show_invite'),
]