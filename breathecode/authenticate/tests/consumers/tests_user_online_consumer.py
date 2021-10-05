import asyncio
import functools
from channels.testing import WebsocketCommunicator
from django.conf.urls import re_path
from channels.routing import URLRouter
from ...consumers import UserOnlineConsumer
from ..mixins import AuthTestCase
from unittest.mock import MagicMock, call, patch


def websocket_comunicator_accept_mock():
    def accept():
        pass

    return MagicMock(side_effect=accept)


def websocket_comunicator_send_json_mock():
    def send_json(obj):
        pass

    return MagicMock(side_effect=send_json)


class UserOnlineConsumerTestSuite(AuthTestCase):
    """
    🔽🔽🔽 Connect
    """
    @patch.object(UserOnlineConsumer, '__init__', new=lambda x: None)
    @patch.object(UserOnlineConsumer, 'accept', new=websocket_comunicator_accept_mock())
    @patch.object(UserOnlineConsumer, 'send_json', new=websocket_comunicator_send_json_mock())
    def test_user_online_consumer__connect__without_data(self):
        instance = UserOnlineConsumer()
        instance.connect()

        self.assertEqual(instance.accept.call_args_list, [call()])
        self.assertEqual(instance.send_json.call_args_list, [call({'status': 'ONLINE'})])

    @patch.object(UserOnlineConsumer, '__init__', new=lambda x: None)
    @patch.object(UserOnlineConsumer, 'accept', new=websocket_comunicator_accept_mock())
    @patch.object(UserOnlineConsumer, 'send_json', new=websocket_comunicator_send_json_mock())
    def test_user_online_consumer__connect__with_data(self):
        model = self.generate_models(profile_academy=True)
        instance = UserOnlineConsumer()
        instance.connect()

        self.assertEqual(instance.accept.call_args_list, [call()])
        self.assertEqual(instance.send_json.call_args_list, [
            call({
                'status': 'ONLINE',
                'id': model.profile_academy.id,
                'email': model.profile_academy.email,
                'first_name': model.profile_academy.first_name,
                'last_name': model.profile_academy.last_name,
                'avatar_url': None,
            })
        ])

    @patch.object(UserOnlineConsumer, '__init__', new=lambda x: None)
    @patch.object(UserOnlineConsumer, 'accept', new=websocket_comunicator_accept_mock())
    @patch.object(UserOnlineConsumer, 'send_json', new=websocket_comunicator_send_json_mock())
    def test_user_online_consumer__connect__with_data__with_profile(self):
        profile_kwargs = {'avatar_url': 'asdasd'}
        model = self.generate_models(profile_academy=True, profile=True, profile_kwargs=profile_kwargs)
        instance = UserOnlineConsumer()
        instance.connect()

        self.assertEqual(instance.accept.call_args_list, [call()])
        self.assertEqual(instance.send_json.call_args_list, [
            call({
                'status': 'ONLINE',
                'id': model.profile_academy.id,
                'email': model.profile_academy.email,
                'first_name': model.profile_academy.first_name,
                'last_name': model.profile_academy.last_name,
                'avatar_url': model.profile.avatar_url,
            })
        ])

    """
    🔽🔽🔽 Disconnect
    """

    @patch.object(UserOnlineConsumer, '__init__', new=lambda x: None)
    @patch.object(UserOnlineConsumer, 'send_json', new=websocket_comunicator_send_json_mock())
    def test_user_online_consumer__disconnect__without_data(self):
        instance = UserOnlineConsumer()
        instance.disconnect(0)

        self.assertEqual(instance.send_json.call_args_list, [call({'status': 'OFFLINE'})])

    @patch.object(UserOnlineConsumer, '__init__', new=lambda x: None)
    @patch.object(UserOnlineConsumer, 'send_json', new=websocket_comunicator_send_json_mock())
    def test_user_online_consumer__disconnect__with_data(self):
        model = self.generate_models(profile_academy=True)
        instance = UserOnlineConsumer()
        instance.disconnect(0)

        self.assertEqual(instance.send_json.call_args_list, [
            call({
                'status': 'OFFLINE',
                'id': model.profile_academy.id,
                'email': model.profile_academy.email,
                'first_name': model.profile_academy.first_name,
                'last_name': model.profile_academy.last_name,
                'avatar_url': None,
            })
        ])

    @patch.object(UserOnlineConsumer, '__init__', new=lambda x: None)
    @patch.object(UserOnlineConsumer, 'send_json', new=websocket_comunicator_send_json_mock())
    def test_user_online_consumer__disconnect__with_data__with_profile(self):
        profile_kwargs = {'avatar_url': 'asdasd'}
        model = self.generate_models(profile_academy=True, profile=True, profile_kwargs=profile_kwargs)
        instance = UserOnlineConsumer()
        instance.disconnect(0)

        self.assertEqual(instance.send_json.call_args_list, [
            call({
                'status': 'OFFLINE',
                'id': model.profile_academy.id,
                'email': model.profile_academy.email,
                'first_name': model.profile_academy.first_name,
                'last_name': model.profile_academy.last_name,
                'avatar_url': model.profile.avatar_url,
            })
        ])

    """
    🔽🔽🔽 Receive
    """

    @patch.object(UserOnlineConsumer, '__init__', new=lambda x: None)
    @patch.object(UserOnlineConsumer, 'send_json', new=websocket_comunicator_send_json_mock())
    def test_user_online_consumer__receive(self):
        instance = UserOnlineConsumer()
        instance.receive('')

        self.assertEqual(instance.send_json.call_args_list,
                         [call({
                             'status': 'ERROR',
                             'message': 'Send message is not allowed'
                         })])
