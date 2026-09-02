import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

        # Check authentication (requires AuthMiddleware and JWT setup in ASGI)
        if self.scope['user'].is_anonymous:
            await self.close()
            return

        # Check if user is participant
        is_participant = await self.is_participant(self.conversation_id, self.scope['user'])
        if not is_participant:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']

        # Save message to database
        saved_message = await self.save_message(self.conversation_id, self.scope['user'], message_text)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_id': saved_message.id,
                'message': message_text,
                'sender_id': self.scope['user'].id,
                'timestamp': str(saved_message.timestamp),
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        message_id = event['message_id']
        timestamp = event.get('timestamp')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'id': message_id,
            'message': message,
            'sender_id': sender_id,
            'timestamp': timestamp
        }))

    @database_sync_to_async
    def is_participant(self, conversation_id, user):
        try:
            conv = Conversation.objects.get(id=conversation_id)
            return conv.participants.filter(id=user.id).exists()
        except Conversation.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, conversation_id, sender, text):
        conv = Conversation.objects.get(id=conversation_id)
        msg = Message.objects.create(conversation=conv, sender=sender, text=text)
        conv.save() # Trigger updated_at
        return msg
