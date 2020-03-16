from django.shortcuts import render

from auction_house.models import Catalog
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from rest_framework import status

from auction_house.modules.auction import make_auctions, online_manager

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
            message = 'Evaluation run at {0}'.format(start)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OnlineAuctionApiView(APIView):
    serializer_class = serializers.OnlineAuctionSeralizer
    def get(self, request, format=None):
        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Its similar to traditional Django view',
            'Gives most control over your logic',
            'Is maped manualy to URLs'
        ]
        return Response({'message': 'Send events here!', 'an_apiview': an_apiview})
    def post(self, request):
        serializer = serializers.OnlineAuctionSeralizer(data=request.data)
        if serializer.is_valid():
            start = serializer.data.get('start')
            online_manager(request, start)
            message = 'Online manager run at {0}'.format(start)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CatalogView(APIView):
    def get(self, request, format=None):
        an_apiview = list()
        for obj in Catalog.objects.all():
            new_dict = dict()
            new_dict["ID"] = obj.pk
            new_dict["code"] = obj.code
            new_dict["description"] = obj.description
            new_dict["type"] = obj.str_type
            an_apiview.append(new_dict)
        return Response({'message': 'Catalog of scrap', 'an_apiview': an_apiview})

    def post(self, request):
        serializer = serializers.CatalogSerializer(data=request.data)
        my_created = 0
        my_updated = 0
        if 'katalog' in request.data:
            for line in request.data.get("katalog"):
                print(line['code'], line['description'])
                code = line['code']
                test = Catalog.objects.filter(code=code)
                if test.count() < 1:
                    data_line = Catalog(
                        code=line['code'],
                        description=line['description'],
                        str_type=line['kind'],
                    )
                    data_line.save()
                    my_created += 1
                else:
                    data_line = test.first()
                    data_line.code = line['code']
                    data_line.description=line['description']
                    data_line.str_type=line['kind']
                    my_updated += 1
                if 'G' in data_line.str_type:
                    data_line.is_group = True
                if 'N' in data_line.str_type:
                    data_line.is_dangerous = True
                data_line.save()
            message = 'Created {} lines. Updated {} lines. [{}]'\
                .format(my_created, my_updated, my_created+my_updated)
            return Response({'message': message})
        else:
            return Response({'message': 'Missinng katalog object'}, status=status.HTTP_400_BAD_REQUEST)
