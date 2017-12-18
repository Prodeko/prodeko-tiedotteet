from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from info.models import *


class MessageSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    class Meta:
        model = Message
        fields = ('__all__')

class CategorySerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'title', 'order', 'messages']

    def get_messages(self, category):
        queryset = Message.visible_objects.filter(category=category)
        serializer = MessageSerializer(queryset, many=True)
        return serializer.data

class ContentList(APIView):
    """
    List all visible content.
    """
    def get(self, request, format=None):
        visible_messages = Message.objects.all().order_by('end_date')
        queryset = Category.objects.all().order_by('order')
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
