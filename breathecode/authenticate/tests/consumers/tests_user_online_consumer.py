import asyncio
import functools
from channels.testing import WebsocketCommunicator
from django.conf.urls import re_path
from channels.routing import URLRouter
from ...consumers import UserOnlineConsumer
from ..mixins import AuthTestCase


class MyTests(AuthTestCase):
    def setUp(self):
        """Before each test"""
        self.generate_models(profile_academy=True)
        print(self.all_profile_academy_dict())

    # def test_my_consumer(self):
    #     self.generate_models(profile_academy=True)
    #     application = URLRouter([
    #         re_path(r'^testws/(?P<message>\w+)/$', UserOnlineConsumer.as_asgi()),
    #     ])

    #     communicator = WebsocketCommunicator(application, '/testws/test/')
    #     connected, subprotocol = self.run_as_sync(communicator.connect)

    async def test_my_consumer(self):
        # # await self.generate_models(profile_academy=True)
        # loop = asyncio.get_event_loop()
        # # loop.run_in_executor(None, self.generate_models, profile_academy=True)
        # loop.run_in_executor(None, functools.partial(self.generate_models, profile_academy=True))
        application = URLRouter([
            re_path(r'^testws/(?P<message>\w+)/$', UserOnlineConsumer.as_asgi()),
        ])

        communicator = WebsocketCommunicator(application, '/testws/test/')
        connected, subprotocol = await communicator.connect()
        assert connected
        self.assertTrue(connected)

        message = await communicator.receive_from()
        assert message == 'test'

        assert False
