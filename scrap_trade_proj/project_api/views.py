from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from rest_framework import status

from auction_house.modules.auction import make_auctions

class HelloApiView(APIView):
    def get(self, request, format=None):
        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Its similar to traditional Django view',
            'Gives most control over your logic',
            'Is maped manualy to URLs'
        ]
        return Response({'message': 'Hello!', 'an_apiview': an_apiview})


class EvaluateAuctionApiView(APIView):
    serializer_class = serializers.EvaluateAuctionSeralizer
    def get(self, request, format=None):
        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Its similar to traditional Django view',
            'Gives most control over your logic',
            'Is maped manualy to URLs'
        ]
        return Response({'message': 'Send events here!', 'an_apiview': an_apiview})
    def post(self, request):
        serializer = serializers.EvaluateAuctionSeralizer(data=request.data)
        if serializer.is_valid():
            start = serializer.data.get('start')
            make_auctions(request, start)
            message = 'Run at {0}'.format(start)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
