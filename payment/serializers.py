from rest_framework import serializers
from .models import PaymentDetails


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetails
        fields = "__all__"