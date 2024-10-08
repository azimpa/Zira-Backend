from rest_framework import serializers
from chat.models import CustomerChat


class CustomerChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerChat
        fields = "__all__"
