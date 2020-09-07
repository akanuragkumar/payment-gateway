from django.db import transaction
from rest_framework import serializers
from jsonschema import validate
from payment_api.models import PaymentMethod, PaymentDetail
import random


class PaymentMethodSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    subtype = serializers.CharField(required=True)
    is_active = serializers.BooleanField(required=False)

    @transaction.atomic()
    def create(self, validated_data):
        # creating new movie collection
        collection = PaymentMethod.objects.create(type=validated_data['type'],
                                                  subtype=validated_data['subtype'])
        return collection


class PaymentDetailSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    currency = serializers.CharField(required=True)
    amount = serializers.FloatField(required=True)
    card = serializers.JSONField(required=True)

    @transaction.atomic()
    def create(self, validated_data):
        # creating new movie collection
        status_randomizer = ["failed", "success"]
        validated_data["status"] = random.choice(status_randomizer)
        collection = PaymentDetail.objects.create(type=validated_data['type'],
                                                  currency=validated_data['currency'],
                                                  amount=validated_data['amount'],
                                                  card=validated_data['card'],
                                                  status=validated_data['status']
                                                  )
        return collection
