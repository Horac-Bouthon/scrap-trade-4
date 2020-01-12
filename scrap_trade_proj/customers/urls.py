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
    CustomerInfoDetailView,
)


urlpatterns = [
    path('', user_views.customer_list, name='project-customer-home'),
    path('register/', user_views.register, name='project-user-register'),
    path('mylogin/', user_views.my_loging_view, name='project-user-mylogin'),
    path('login/', auth_views.LoginView.as_view(template_name='customers/login.html'), name='project-user-login'),
    path('logout/', user_views.my_logout_view, name='project-user-logout'),
    path('user/profile/', user_views.user_profile, name='project-user-profile'),
    path('<int:pk>/info/', CustomerInfoDetailView.as_view(), name='project-customer-info'),
    path('<int:pk>/profile/', CustomerDetailView.as_view(), name='project-customer-detail'),
    path('new/', CustomerCreateView.as_view(), name='project-customer-new'),
    path('<int:pk>/update/', CustomerUpdateView.as_view(), name='project-customer-update'),
    path('<int:pk>/delete/', CustomerDeletelView.as_view(), name='project-customer-delete'),
    path('<int:pk>/email/<int:pk2>', user_views.customer_email_update, name='project-customer-email-update'),
    path('<int:pk>/email/new', user_views.customer_email_create, name='project-customer-email-create'),
    path('<int:pk>/delete-email/', CustomerDeletelEmail.as_view(), name='project-email-delete'),
    path('<int:pk>/web/<int:pk2>', user_views.customer_web_update, name='project-customer-web-update'),
    path('<int:pk>/web/new', user_views.customer_web_create, name='project-customer-web-create'),
    path('<int:pk>/delete-web/', CustomerDeletelWeb.as_view(), name='project-web-delete'),
    path('<int:pk>/phone/<int:pk2>', user_views.customer_phone_update, name='project-customer-phone-update'),
    path('<int:pk>/phone/new', user_views.customer_phone_create, name='project-customer-phone-create'),
    path('<int:pk>/delete-phone/', CustomerDeletelPhone.as_view(), name='project-phone-delete'),
    path('<int:pk>/bank/<int:pk2>', user_views.customer_bank_update, name='project-customer-bank-update'),
    path('<int:pk>/bank/new', user_views.customer_bank_create, name='project-customer-bank-create'),
    path('<int:pk>/delete-bank/', CustomerDeletelBank.as_view(), name='project-bank-delete'),
    path('<int:pk>/est/<int:pk2>', user_views.customer_est_update, name='project-customer-est-update'),
    path('<int:pk>/est/new', user_views.customer_est_create, name='project-customer-est-create'),
    path('<int:pk>/delete-est/', CustomerDeletelEst.as_view(), name='project-est-delete'),
    path('<int:pk>/user/<int:pk2>', user_views.customer_user_update, name='project-customer-user-update'),
    path('<int:pk>/user/new', user_views.customer_user_create, name='project-customer-user-create'),
    path('<int:pk>/tran/<str:lang>/', user_views.customer_tran_update, name='project-customer-tran'),
]
