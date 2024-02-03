from channels.consumer import AsyncConsumer,SyncConsumer,async_to_sync
from channels.exceptions import StopConsumer
# from asgiref.sync import async_to_sync
from time import sleep
import json
class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        global group_name
        group_name=self.scope['url_route']['kwargs']['group_name']
        print("connected",event)
        print("hello",group_name)

        async_to_sync(self.channel_layer.group_add)(group_name,self.channel_name)

        self.send({
            'type':'websocket.accept'
        })

    def websocket_receive(self,event):
        if self.scope['user'].is_authenticated:

            print("received++++++++++++",event['text'])
            print("channel name",self.channel_name)
            print("channel layer",self.channel_layer)
            # for x in range(10):
            #     self.send({
            #         'type':'websocket.send',
            #         'text':str(x)
            #     })
            async_to_sync(self.channel_layer.group_send)(group_name,{
                'type':'chat.message',
                'message':event['text']
            })
        else:
            async_to_sync(self.channel_layer.group_send)(group_name,{
                'type':'chat.message',
                'message':json.dumps({"msg":"Login is required"})
            })


    def chat_message(self,event):
        print(event)
        if self.scope['user'].is_authenticated:

            self.send({
                'type':'websocket.send',
                'text':event['message']
            })
        else:
            self.send({
                'type':'websocket.send',
                'text':json.dumps({"msg":"Login is required"})
            })
    def websocket_disconnect(self,event):
        print("disconnected",event)
        async_to_sync(self.channel_layer.group_discard)(group_name,self.channel_name)
        
        raise StopConsumer()

# class MySyncConsumer(AsyncConsumer):
#     async def websocket_connect(self,event):
#         print("hello",self.scope['url_route']['kwargs']['group_name'])
#         print("connected",event)
#         await self.channel_layer.group_add('programmers',self.channel_name)

#         await self.send({
#             'type':'websocket.accept'
#         })

#     async def websocket_receive(self,event):

#         print("received++++++++++++",event['text'])
#         print("channel name",self.channel_name)
#         print("channel layer",self.channel_layer)
#         # for x in range(10):
#         #     self.send({
#         #         'type':'websocket.send',
#         #         'text':str(x)
#         #     })
#         await self.channel_layer.group_send('programmers',{
#             'type':'chat.message',
#             'message':event['text']
#         })

#     async def chat_message(self,event):
#         print(event)
#         await self.send({
#             'type':'websocket.send',
#             'text':event['message']
#         })

#     async def websocket_disconnect(self,event):
#         print("disconnected",event)
#         await self.channel_layer.group_discard('programmers',self.channel_name)
        
#         raise StopConsumer()


# # class MySyncConsumer(AsyncConsumer):
# #     async def websocket_connect(self,event):
# #         print("connected",event)
# #         print("channel layer",self.channel_layer)      
# #         self.channel_name="heloo"
# #         print("channel lay",self.channel_name)

# #         self.channel_layer.group_add('programmers',self.channel_layer)
# #         # print(self.channel_layer.)
# #         await self.send({
# #             'type':'websocket.accept'
# #         })

# #     async def websocket_receive(self,event):
# #         print("received++++++++++++",event)
# #         print(event['text'])
# #         self.send("hello",self.channel_name)
# #         for x in range(10):
# #             await self.send({
# #                 'type':'websocket.send',
# #                 'text':str(x)
# #             })
# #             await asyncio.sleep(1)
            

# #     async def websocket_disconnect(self,event):
# #         print("disconnected",event)
# #         self.channel_layer.group_discard('programmers',self.channel_name)
# #         raise StopConsumer()