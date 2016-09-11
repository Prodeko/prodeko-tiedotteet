from rest_framework import generics, permissions
from info.models import *
from info.serializers import *


class ContentList(generics.ListAPIView):
    """
    List all visible content.
    """
    visible_messages = Message.visible_objects.order_by('end_date')
    queryset = Category.objects.filter(messages__in=visible_messages).distinct().order_by('order')
    serializer_class = ContentSerializer

class MessageList(generics.ListAPIView):
    """
    List all visible messages.
    """
    queryset = Message.visible_objects.order_by('end_date')
    serializer_class = MessageSerializer
