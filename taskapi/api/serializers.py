from rest_framework import serializers
from rest_framework.serializers import ValidationError

def positive_value(value):
    if value < 1:
        raise serializers.ValidationError('This field must be greater or equal than 1.')

class VerifySerializers(serializers.Serializer):
    USER_CHOICES =( 
    ("user1", "user1"), 
    ("user2", "user2"),
    )
    STOCK_CHOICES =( 
    ("stock1", "stock1"), 
    ("stock2", "stock2"),
    ("stock3", "stock3"),
    )
    user = serializers.ChoiceField(choices=USER_CHOICES)
    stockname = serializers.ChoiceField(choices=STOCK_CHOICES)
    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError('This field must be greater or equal than 1.')
        return value
