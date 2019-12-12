from rest_framework import serializers
from datetime import datetime

class EvaluateAuctionSeralizer(serializers.Serializer):
    start = serializers.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S",'iso-8601',], 
        initial=datetime.now(),
    )
