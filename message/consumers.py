import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .serializer import MessageSerializer
from .models import Message
from employee.models import Employee
from booking.models import Booking
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        booking_id = self.scope["url_route"]["kwargs"]["id"]
        
        self.room_name = (
            booking_id
        )
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await super().disconnect(close_code)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]
        sender = data["sender"]
        user_id = data["user"]
        employee_id = data["employee"]
        user = await self.get_user(user_id)
        employee = await self.get_employee(employee_id)
        await self.save_message(
            sender=sender, user=user,employee=employee, message=message, thread_name=self.room_group_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "sender": sender,
                }
            )
        )
    
    @database_sync_to_async
    def get_user(self, user_id):
        return get_user_model().objects.filter(id=user_id).first()
    
        
    @database_sync_to_async
    def get_employee(self, employee_id):
        return Employee.objects.filter(employee__id=employee_id).first()

    @database_sync_to_async
    def save_message(self, user,employee, sender, message, thread_name):
        if Booking.objects.filter(id=thread_name.split('chat_')[1])[0].chat_flag == False and sender == 'employee':
            obj = Booking.objects.get(id=thread_name.split('chat_')[1])
            obj.chat_flag = True 
            obj.save()
        Message.objects.create(sender=sender,user=user,employee=employee, message=message, thread_name=thread_name)