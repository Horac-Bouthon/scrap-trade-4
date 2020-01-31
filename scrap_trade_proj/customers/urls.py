from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as user_views
from . views import (
    CustomerDetailView,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerDeletelView,
    CustomerDeletelEmail,
    CustomerDeletelWeb,
    CustomerDeletelPhone,
    CustomerDeletelBank,
    CustomerDeletelEst,
)


urlpatterns = [
    path('', user_views.CustomerList.as_view(), name='project-customer-home'),
    
    path('user/login/', user_views.log_in, name='user-login'),
    path('user/logout/', user_views.log_out, name='user-logout'),
    path('user/edit-profile/', user_views.profile, name='user-profile'),    
    
    
    path('user/reset-password/',
         user_views.request_password_reset_link, 
         name="user-reset-request"),
    
    path('user/reset-password/<str:uuid>', 
         user_views.reset_password, 
         name="user-reset"),

    
    path('new/', CustomerCreateView.as_view(), name='project-customer-new'),
    path('<int:pk>/details/', user_views.CustomerInfo.as_view(), name='project-customer-info'),
    path('<int:pk>/edit/', CustomerDetailView.as_view(), name='project-customer-detail'),
    path('<int:pk>/edit-main/', CustomerUpdateView.as_view(), name='project-customer-update'),
    path('<int:pk>/confirm-delete/', CustomerDeletelView.as_view(), name='project-customer-delete'),
    
    path('<int:pk>/translations/<str:lang>/', user_views.customer_tran_update, name='project-customer-tran'),
    
    path('<int:pk>/email/new', user_views.customer_email_create, name='project-customer-email-create'),
    path('<int:pk>/email/<int:pk2>', user_views.customer_email_update, name='project-customer-email-update'),
    path('<int:pk>/email/confirm-delete/', CustomerDeletelEmail.as_view(), name='project-email-delete'),
    
    path('<int:pk>/web/new/', user_views.customer_web_create, name='project-customer-web-create'),
    path('<int:pk>/web/<int:pk2>', user_views.customer_web_update, name='project-customer-web-update'),
    path('<int:pk>/web/confirm-delete/', CustomerDeletelWeb.as_view(), name='project-web-delete'),
    
    path('<int:pk>/phone/new/', user_views.customer_phone_create, name='project-customer-phone-create'),
    path('<int:pk>/phone/<int:pk2>', user_views.customer_phone_update, name='project-customer-phone-update'),
    path('<int:pk>/phone/confirm-delete/', CustomerDeletelPhone.as_view(), name='project-phone-delete'),
    
    path('<int:pk>/bank/new/', user_views.customer_bank_create, name='project-customer-bank-create'),
    path('<int:pk>/bank/<int:pk2>', user_views.customer_bank_update, name='project-customer-bank-update'),
    path('<int:pk>/bank/confirm-delete/', CustomerDeletelBank.as_view(), name='project-bank-delete'),
    
    path('<int:pk>/est/new/', user_views.customer_est_create, name='project-customer-est-create'),
    path('<int:pk>/est/<int:pk2>', user_views.customer_est_update, name='project-customer-est-update'),
    path('<int:pk>/est/confirm-delete/', CustomerDeletelEst.as_view(), name='project-est-delete'),
    
    path('<int:pk>/user/new', user_views.customer_user_create, name='project-customer-user-create'),
    path('<int:pk>/user/<int:pk2>', user_views.customer_user_update, name='project-customer-user-update'),
    
]
