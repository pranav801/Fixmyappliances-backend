from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import Message



class MessageSerializer(ModelSerializer):
    sender = SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id','message','sender']

    def get_sender(self,obj):
        return obj.sender
