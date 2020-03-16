from rest_framework import serializers
from datetime import datetime

class EvaluateAuctionSeralizer(serializers.Serializer):
    start = serializers.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S",'iso-8601',],
        initial=datetime.now(),
    )

class OnlineAuctionSeralizer(serializers.Serializer):
    start = serializers.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S",'iso-8601',],
        initial=datetime.now(),
    )

class CatalogSerializer(serializers.Serializer):
    products = serializers.ListField(
        child=serializers.CharField(max_length=1500),
        allow_empty=True,
        )
