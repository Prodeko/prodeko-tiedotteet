from info.models import *
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    class Meta:
        model = Message
        fields = ('__all__')



class ContentSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ('__all__')

    def get_messages(self, category):
        messages = Message.visible_objects.filter(category=category)
        serializer = MessageSerializer(instance=messages, many=True)
        return serializer.data


class MessageSerializerDev(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    class Meta:
        model = Message
        fields = ('__all__')

class ContentSerializerDev(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ('__all__')

    def get_messages(self, category):
        messages = Message.objects.filter(category=category)[:5]
        serializer = MessageSerializer(instance=messages, many=True)
        return serializer.data
