from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('predict_form', views.predict, name='predict_form'),
    path('predict_loan/', views.predict_loan, name='predict_loan'),
    path('prediction_result/', views.prediction_result, name='prediction_result'),
    path('non-risky-loans/', views.non_risky_loans, name='non_risky_loans'),
    path('risky-loans/', views.risky_loans, name='risky_loans'),
]
