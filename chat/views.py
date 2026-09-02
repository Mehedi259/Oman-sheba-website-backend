from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return conversations where user is a participant, ordered by last updated
        return Conversation.objects.filter(participants=self.request.user).order_by('-updated_at')

class ConversationMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        conversation = generics.get_object_or_404(Conversation, id=conversation_id, participants=self.request.user)
        
        # Mark unread messages as read
        conversation.messages.filter(is_read=False).exclude(sender=self.request.user).update(is_read=True)
        
        return conversation.messages.all()

class InitiateConversationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user_id')
        related_object_type = request.data.get('related_object_type')
        related_object_id = request.data.get('related_object_id')

        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'Target user not found'}, status=status.HTTP_404_NOT_FOUND)

        if target_user == request.user:
            return Response({'error': 'Cannot start a conversation with yourself'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if conversation already exists for these users and this object
        convs = Conversation.objects.filter(participants=request.user).filter(participants=target_user)
        if related_object_type and related_object_id:
            conv = convs.filter(related_object_type=related_object_type, related_object_id=related_object_id).first()
        else:
            # Generic chat between two users
            conv = convs.filter(related_object_type__isnull=True).first()

        if not conv:
            conv = Conversation.objects.create(
                related_object_type=related_object_type,
                related_object_id=related_object_id
            )
            conv.participants.add(request.user, target_user)

        serializer = ConversationSerializer(conv, context={'request': request})
        return Response(serializer.data)
