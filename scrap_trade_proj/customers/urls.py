from django.urls import path, include
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
    
    # User management
    path('user/', include([
        path('new/', CustomerCreateView.as_view(), name='project-customer-new'),  # @todo; Validate if it's needed
        path('login/', user_views.log_in, name='user-login'),
        path('logout/', user_views.log_out, name='user-logout'),
        path('reset-password/', include([
            path('', 
                 user_views.request_password_reset_link, 
                 name="user-reset-request"),
            path('<str:uuid>',
                 user_views.reset_password, 
                 name="user-reset"),
        ])),
        
        path('edit-profile/', user_views.profile, name='user-profile'),
    ])),

    # Customers
    path('', user_views.CustomerList.as_view(), name='project-customer-home'), # @todo; Rename `name` to `customer list` or something
    path('<int:pk>/', include([
        
        path('', user_views.CustomerInfo.as_view(), name='project-customer-info'),
        
        path('delete/', CustomerDeletelView.as_view(), name='project-customer-delete'),
        
        path('create-new-user', user_views.customer_user_create, name='project-customer-user-create'),
        path('modify-user/<int:pk2>', user_views.customer_user_update, name='project-customer-user-update'),
        
        # Editing customer info
        path('edit/', include([
            
            path('', CustomerDetailView.as_view(), name='project-customer-detail'),
            
            path('details/', CustomerUpdateView.as_view(), name='project-customer-update'),
            path('translations/<str:lang>/', user_views.customer_tran_update, name='project-customer-tran'),  # @todo; Add a link to translations into the customer edit page
            path('email/', include([
                path('<int:pk2>', user_views.customer_email_update, name='project-customer-email-update'),
                path('create', user_views.customer_email_create, name='project-customer-email-create'),
                path('delete', CustomerDeletelEmail.as_view(), name='project-email-delete'),
            ])),
            path('web/', include([
                path('<int:pk2>', user_views.customer_web_update, name='project-customer-web-update'),
                path('create', user_views.customer_web_create, name='project-customer-web-create'),
                path('delete', CustomerDeletelWeb.as_view(), name='project-web-delete'),
            ])),
            path('phone/', include([
                path('<int:pk2>', user_views.customer_phone_update, name='project-customer-phone-update'),
                path('create', user_views.customer_phone_create, name='project-customer-phone-create'),
                path('delete', CustomerDeletelPhone.as_view(), name='project-phone-delete'),
            ])),
            path('bank/', include([
                path('create', user_views.customer_bank_create, name='project-customer-bank-create'),
                path('<int:pk2>', user_views.customer_bank_update, name='project-customer-bank-update'),
                path('delete', CustomerDeletelBank.as_view(), name='project-bank-delete'),
            ])),
            path('est/', include([
                path('create', user_views.customer_est_create, name='project-customer-est-create'),
                path('<int:pk2>', user_views.customer_est_update, name='project-customer-est-update'),
                path('delete', CustomerDeletelEst.as_view(), name='project-est-delete'),
            ])),
        ])),
    ])),
]
