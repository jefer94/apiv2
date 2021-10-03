from channels.testing import WebsocketCommunicator
from django.conf.urls import re_path
from channels.routing import URLRouter
from ...consumers import UserOnlineConsumer
from ..mixins import AuthTestCase


class MyTests(AuthTestCase):
    def test_my_consumer(self):
        self.generate_models(profile_academy=True)
        application = URLRouter([
            re_path(r'^testws/(?P<message>\w+)/$', UserOnlineConsumer.as_asgi()),
        ])

        communicator = WebsocketCommunicator(application, '/testws/test/')
        # connected, subprotocol = await communicator.connect()
        connected, subprotocol = communicator.connect()
        # assert connected
        # self.assertTrue(connected)

        # message = await communicator.receive_from()
        # assert message == 'test'

        # assert False
