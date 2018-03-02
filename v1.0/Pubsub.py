class PubSub:  # how to map id to object?
    def __init__(self):

        self.publishers = dict()
        self.channels = dict()
        self.subscribers = dict()
        self.channel_to_subscriber = dict()

    '''
    def register_publishers(self, list_of_publishers):
        for publisher in list_of_publishers:
            publisher.register()

    def register_channels(self, list_of_channels):
        for channel in list_of_channels:
            channel.register()


    def register_subscribers(self, list_of_subscribers):
        for subscriber in list_of_subscribers:
            subscriber.register()

    def subscribe(channel_id, subscriber_id):
        if channel_id in self.channel_to_subscriber:
            self.channel_to_subscriber[channel_id].append(subscriber_id)
        else:
            self.channel_to_subscriber[channel_id] = [subscriber_id]

        #ligra.subscribe(channel_id, subscriber_id)
    '''


class Broker:
    def __init__(self): pass

    def add_publisher(self, publisher_id): return

    def add_channel(self, channel_name): return

    def add_subscriber(self, subscriber_id): return

    def add_subscription(self, subscriber_id, channel_name): return


class Publisher:
    def __init__(self, publisher_id):
        self.id = publisher_id
        self.broker = None

    def publish(self, event, channel_name):
        if not event:
            raise ValueError("Event is empty!")
        return

    def register(self, broker):
        broker.add_publisher(self.id)
        self.broker = broker


class Channel:
    def __init__(self, channel_name):
        self.name = channel_name

    def register(self, broker):
        broker.add_channel(self.name)


class Subscriber:
    def __init__(self, subscriber_id):
        self.id = subscriber_id
        self.callback_function = None
        self.broker = None

    def register(self, callback_function, broker):
        self.callback_function = callback_function
        broker.add_subscriber(self.id)
        self.broker = broker

    def subscribe(self, channel_name):
        if self.broker:
            self.broker.add_subscription(self.id, channel_name)
        else:
            raise ValueError("You must first register with a broker!")
