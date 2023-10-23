from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import Message



class MessageSerializer(ModelSerializer):
    sender_username = SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message','sender_username']

    def get_sender_username(self,obj):
        return obj.sender.username

class ChatListSerializer(ModelSerializer):
    user_profile = SerializerMethodField()
    username = SerializerMethodField()

    class Meta:
        model = Message
        fields = ['user_profile','username']

    def get_username(self,obj):
        return obj
    
    # def get_user_profile(self,obj):
    #     return UserProfileSerializer(UserProfile.objects.filter(user__username=obj).first()).data.get('profile_image')