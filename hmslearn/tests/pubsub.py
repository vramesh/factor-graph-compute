import unittest
import mock
from Pubsub import Publisher, Broker, Channel, Subscriber


class TestPublisher(unittest.TestCase):
    @mock.patch('pubsub.Broker')
    def setUp(self, mock_broker):
        self.broker = mock_broker.return_value

        publisher_id = 0
        self.publisher = Publisher(publisher_id)

    def tearDown(self):
        pass

    def test_publish_success(self):
        event = 'hello'
        channel_name = 'test channel'
        self.assertIsNone(self.publisher.publish(event, channel_name))

    def test_publish_event_is_none(self):
        self.assertRaises(ValueError, self.publisher.publish, None, None)

    def test_register(self):
        self.assertIsNone(self.publisher.register(self.broker))
        self.assertEqual(self.publisher.broker, self.broker)

    def test_register_with_broker_exception(self):
        self.broker.add_publisher.side_effect = Exception()
        self.assertRaises(Exception, self.publisher.register, self.broker)


class TestChannel(unittest.TestCase):
    @mock.patch('pubsub.Broker')
    def setUp(self, mock_broker):
        self.broker = mock_broker.return_value

        channel_name = 'test channel'
        self.channel = Channel(channel_name)

    def tearDown(self):
        pass

    def test_register(self):
        self.assertIsNone(self.channel.register(self.broker))

    def test_register_with_broker_exception(self):
        self.broker.add_channel.side_effect = Exception()
        self.assertRaises(Exception, self.channel.register, self.broker)


class TestSubscriber(unittest.TestCase):

    @mock.patch('pubsub.Broker')
    def setUp(self, mock_broker):
        subscriber_id = 0
        self.subscriber = Subscriber(subscriber_id)
        self.broker = mock_broker.return_value
        self.callback_function = lambda x, y: x + y

    def tearDown(self):
        pass

    def test_register(self):  # , mock_broker):
        self.assertIsNone(self.subscriber.register(
            self.callback_function, self.broker))

    def test_register_with_broker_exception(self):
        self.broker.add_subscriber.side_effect = Exception()
        self.assertRaises(Exception, self.subscriber.register,
                          self.callback_function, self.broker)

    def test_subscribe(self):
        self.subscriber.register(self.callback_function, self.broker)
        self.assertIsNone(self.subscriber.subscribe('test channel'))

    def test_subscribe_before_registration(self):
        self.assertRaises(
            ValueError, self.subscriber.subscribe, 'test channel')

    def test_subscribe_with_broker_exception(self):
        self.subscriber.register(self.callback_function, self.broker)
        self.broker.add_subscription.side_effect = Exception()
        self.assertRaises(Exception, self.subscriber.subscribe, 'test channel')

    def test_subscribe_when_channel_does_not_exist(self):
        pass


if __name__ == '__main__':
    unittest.main()
