import json
import asyncio
from channels.consumer import AsyncConsumer
from account.models import User
from channels.db import database_sync_to_async
from .models import ReviewRating, Version, Product
import re
import datetime


class ReviewConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        url = self.scope['url_route']['kwargs']['slug_pro']
        regex = int(re.search("[-][0-9]{1,3}[gb|GB]", url).span()[0])
        room_product = url[0:regex]
        self.room_product = room_product
        self.room_group_product = 'comment_%s' % self.room_product
        await self.channel_layer.group_add(
            self.room_group_product,
            self.channel_name
        )

        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        print("received", event)
        font_text = event.get('text', None)
        if font_text is not None:
            loaded_dict_data = json.loads(font_text)
            vote = loaded_dict_data.get('rating')
            comment = loaded_dict_data.get('comment')
            subject = loaded_dict_data.get('subject')
            time = loaded_dict_data.get('time')
            user = self.scope['user']
            if user.is_authenticated:
                name = user.full_name
            
            myResponse = {
                'vote': vote,
                'comment': comment,
                'subject': subject,
                'name': name,
                'time': time,
            }
            await self.create_review_rating(user, subject, comment, vote)
            await self.channel_layer.group_send(
                self.room_group_product,
                {
                    "type": "chat_message",
                    "text": json.dumps(myResponse)
                }
            )
    
    async def websocket_disconnect(self, event):
        print("disconnected", event)
    

    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']           
        })

    @database_sync_to_async
    def create_review_rating(self, user, subject, comment, vote):
        slug = self.scope['url_route']['kwargs']['slug_pro']
        product = Product.objects.get(slug=slug)
        return ReviewRating.objects.create(version=product.version, user=user, subject=subject, review=comment, rating=vote)