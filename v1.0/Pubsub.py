from pubsub_temp import RedisBroker

class PubSub:  # how to map id to object?
    def __init__(self,pubsub_choice="redis"):
        self.publishers = dict() #populated nodes
        self.subscribers = dict() #populated nodes
        self.channels = dict() #populated edges

        if pubsub_choice == "redis":
            self.broker = RedisBroker()

    #these are called during FG.initialize_nodes_and_edges
    def register_subscriber(self, subscriber_id, callback_function):
        self.broker.add_subscriber(subscriber_id, callback_function)

    #these are called during FG.initialize_nodes_and_edges
    def register_publisher(self, publisher_id):
        self.broker.add_publisher(publisher_id)

    #these are called during FG.initialize_nodes_and_edges
    def register_channel(self, channel_id):
        self.broker.add_channel(channel_id)

    def register_subscription(self, subscriber_id, channel_id):
        self.broker.add_subscription(subscriber_id, channel_id)

    #this is called during FG.create() after initialization
    def start(self):
        self.broker.start()



class Broker:
    def __init__(self): pass

    def add_publisher(self, publisher_id): return

    def add_channel(self, channel_name): return

    def add_subscriber(self, subscriber_id): return

    def add_subscription(self, subscriber_id, channel_name): return

#when initialize class, assume is already registered in broker?
'''
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
'''
