from redis_broker import RedisBroker
from redis import Redis

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
        r = Redis() #not sure why this is here
        self.broker.add_channel(channel_id)

    def register_subscription(self, subscriber_id, channel_id):
        self.broker.add_subscription(subscriber_id, channel_id)

    #this is called during FG.create() after initialization
    def start(self):
        self.broker.start()

    def publish(self, channel_id, message):
        self.broker.publish(channel_id,message)

