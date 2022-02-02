import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MovieConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    print("connected")
    await self.accept()