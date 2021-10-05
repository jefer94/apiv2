import json
from channels.generic.websocket import JsonWebsocketConsumer
from breathecode.authenticate.models import ProfileAcademy
# from asgiref.sync import sync_to_async


class UserOnlineConsumer(JsonWebsocketConsumer):
    groups = ['broadcast']

    def get_user(self):
        return ProfileAcademy.objects.filter().first()

    def connect(self):
        result = {'status': 'ONLINE'}
        self.accept()

        # print(dir(self))
        # print('=========================')
        # print(vars(self))
        # print('=========================')
        # print(self.scope)
        # print('=========================')
        # print(self.scope['user'])
        # print('=========================')
        # print(self.groups)
        # print('=========================')
        # print(dir(self.channel_layer))

        pa = self.get_user()
        if pa:
            result['id'] = pa.id
            result['email'] = pa.email
            result['first_name'] = pa.first_name
            result['last_name'] = pa.last_name
            result['avatar_url'] = None

            if pa.user and hasattr(pa.user, 'profile') and pa.user.profile.avatar_url:
                result['avatar_url'] = pa.user.profile.avatar_url

        self.send_json(result)
        # print(self.channel_layer.send.__code__.co_varnames)
        self.channel_layer.send(result)

    def disconnect(self, close_code):
        result = {'status': 'OFFLINE'}

        pa = ProfileAcademy.objects.filter().first()
        if pa:
            result['id'] = pa.id
            result['email'] = pa.email
            result['first_name'] = pa.first_name
            result['last_name'] = pa.last_name
            result['avatar_url'] = None

            if pa.user and hasattr(pa.user, 'profile') and pa.user.profile.avatar_url:
                result['avatar_url'] = pa.user.profile.avatar_url

        self.send_json(result)

    def receive(self, text_data):
        self.send_json({'status': 'ERROR', 'message': 'Send message is not allowed'})
