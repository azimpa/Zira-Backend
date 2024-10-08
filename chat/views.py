from .serializers import CustomerChatSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model
from chat.models import CustomerChat
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class UserToInstructorChatListApi(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    model = CustomerChat
    serializer_class = CustomerChatSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')

        if self.request.user.id > int(user_id):
            group_name = f'chat_{self.request.user.id}-{user_id}'
        else:
            group_name = f'chat_{user_id}-{self.request.user.id}'
        messages = CustomerChat.objects.filter(group_name=group_name)
        messages.update(is_read=True)
        return messages


class UserMessagesView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = CustomerChatSerializer

    def get_queryset(self):
        user_id = self.kwargs['current_user_id']  
        queryset = CustomerChat.objects.filter(Q(user=user_id) | Q(other_user=user_id)).order_by('-time').distinct()

        return queryset


class ChatHistoryWithId(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = CustomerChatSerializer

    def get_queryset(self):
        chat_id = self.kwargs.get('pk')
        return CustomerChat.objects.filter(id=chat_id)