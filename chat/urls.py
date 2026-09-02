from django.urls import path
from .views import ConversationListView, ConversationMessageListView, InitiateConversationView

urlpatterns = [
    path('conversations/', ConversationListView.as_view(), name='conversation-list'),
    path('conversations/<int:conversation_id>/messages/', ConversationMessageListView.as_view(), name='conversation-messages'),
    path('conversations/initiate/', InitiateConversationView.as_view(), name='conversation-initiate'),
]
