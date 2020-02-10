from django.urls import path
from . import views

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('evaluate-auction/', views.EvaluateAuctionApiView.as_view()),
    path('online-auction/', views.OnlineAuctionApiView.as_view()),
]
