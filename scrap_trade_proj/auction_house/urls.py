from django.urls import path
from . import views as ah_views
from . views import (
    AhOfferListView,
    AhAnswerListView,
    AhOfferUpdateView,
    AhOfferDetailView,
    AhOfferDeleteView,
    AhAnswerDeletelView,
    AhOfferInfoView,
    AhDeletelOfferLine,
    AhMatClassDetailView,
    AhOfferCustomerUpdateView,
    AhAnswerDetailView,
    AhAnswerUpdateView,
    AhAnswerCustomerUpdateView,
    AhOfferListForAcceptView,
)


urlpatterns = [
    path('power/offer_list/', AhOfferListView.as_view(), name='ah-offer-list'),

    path('power/offer_list_accept/', AhOfferListForAcceptView.as_view(), name='ah-offer-list-accept'),

    path('power/answer_list/', AhAnswerListView.as_view(), name='ah-answer-list'),
    path('power/<int:pk>/offer_detail', AhOfferDetailView.as_view(), name='ah-offer-detail'),
    path('power/<int:pk>/offer_update', AhOfferUpdateView.as_view(), name='ah-offer-update'),
    path('power/<int:pk>/cust_update', AhOfferCustomerUpdateView.as_view(), name='ah-offer-customer-update'),
    path('power/<int:pk>/offer_delete', AhOfferDeleteView.as_view(), name='ah-offer-delete'),
    path('power/<int:pk>/answer_delete', AhAnswerDeletelView.as_view(), name='ah-answer-delete'),
    path('power/<int:pk>/offer_update-line/<int:pk2>', ah_views.ah_offer_line_update, name='ah-offer-line-update'),
    path('power/<int:pk>/offer_create-line', ah_views.ah_offer_line_create, name='ah-offer-line-create'),
    path('power/offer_delete-line/<int:pk>', AhDeletelOfferLine.as_view(), name='ah-offer-line-delete'),
    path('power/mat_class/<int:pk>', AhMatClassDetailView.as_view(), name='ah-mat-class-detail'),
    path('power/<int:pk>/answer_update', AhAnswerUpdateView.as_view(), name='ah-answer-update'),
    path('customer/<int:pk>/auction', ah_views.ah_customer_auction, name='ah-customer-auction'),
    path('customer/<int:pk>/create_offer', ah_views.ah_customer_offers_create, name='ah-customer-create-offers'),

    path('customer/<int:pk>/offer_change_state/<int:pk2>/<int:pk3>', ah_views.ah_offers_change_state, name='ah-offer-change-state'),
    path('power/<int:pk>/offer_create_step', ah_views.ah_offer_step_create, name='ah-offer-step-create'),
    path('customer/<int:pk>/answer_change_state/<int:pk2>/<int:pk3>', ah_views.ah_answer_change_state, name='ah-answer-change-state'),
    path('power/<int:pk>/answer_create_step', ah_views.ah_answer_step_create, name='ah-answer-step-create'),
    path('customer/<int:pk>/answers/<str:sk>', ah_views.ah_customer_answer_by_state_key, name='ah-customer-state-answers'),
    path('customer/<int:pk>/offers/<str:sk>', ah_views.ah_customer_offers_by_state_key, name='ah-customer-state-offers'),

    path('customer/<int:pk>/answer_detail', AhAnswerDetailView.as_view(), name='ah-answer-detail'),
    path('customer/<int:pk>/answer_update', AhAnswerCustomerUpdateView.as_view(), name='ah-answer-customer-update'),
    path('customer/<int:pk>/answers_line_ppu/<int:pk2>', ah_views.ah_answer_line_update_ppu, name='ah-customer-answers-line-ppu'),
    path('customer/<int:pk>/answers_line_total/<int:pk2>', ah_views.ah_answer_line_update_total, name='ah-customer-answers-line-total'),
    path('customer/<int:pk>/answers_waiting_offers', ah_views.ah_customer_answer_waiting_offers, name='ah-customer-waiting-offers'),
    path('customer/<int:pk>/offer_info', AhOfferInfoView.as_view(), name='ah-offer-info'),
    path('customer/<int:pk>/answers_create/<int:pk2>', ah_views.ah_customer_answer_create, name='ah-customer-answers-create'),

    path('auction/<int:pk2>/<int:pk>/',
         ah_views.realtime_auction,
         name='realtime-auction'),
    path('auction/<int:pk>/',
         ah_views.realtime_auction_info,
         name='realtime-auction-info'),
    path('auction/<int:pk>/line_ppu/<int:pk2>/',
         ah_views.ah_answer_online_update_ppu,
         name='ah-customer-answers-online-ppu'),

]
