from django.urls import path
from . import views

urlpatterns = [
    path("history/", views.UserToInstructorChatListApi.as_view(), name="get-chat-history"),
    path("history/<int:pk>/", views.ChatHistoryWithId.as_view(), name="get-chat-history-id"),
    path("userfrommessage/<int:current_user_id>/", views.UserMessagesView.as_view(), name="user-from-message"),
]
