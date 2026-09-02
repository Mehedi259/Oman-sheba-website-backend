from rest_framework import serializers
from .models import Conversation, Message
from users.models import User

class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'profile_picture']

class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.IntegerField(source='sender.id', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender_id', 'text', 'is_read', 'timestamp']
        read_only_fields = ['id', 'sender_id', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserChatSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'related_object_type', 'related_object_id', 'created_at', 'updated_at', 'last_message', 'unread_count']

    def get_last_message(self, obj):
        msg = obj.messages.last()
        if msg:
            return MessageSerializer(msg).data
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0
