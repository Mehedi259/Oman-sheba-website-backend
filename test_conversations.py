import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheba_backend.settings')
django.setup()

from chat.models import Conversation
from chat.serializers import ConversationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.first()

if not user:
    print("No user found")
else:
    convs = Conversation.objects.filter(participants=user)
    if convs.exists():
        try:
            serializer = ConversationSerializer(convs, many=True)
            print(serializer.data)
            print("Serialization successful!")
        except Exception as e:
            import traceback
            traceback.print_exc()
    else:
        print("No conversations for user")

