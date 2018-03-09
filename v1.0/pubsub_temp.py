import redis
import time

class PubsubRedis:
    def __init__(self):
        self.redis_main = redis.StrictRedis(host='localhost',port=6379, db=0, decode_responses=True)
        self.publishers = set()
        self.channels = list()
        self.subscribers = dict()

    def add_publisher(publisher_id):
        if publisher_id in self.publishers:
            return "Need unique publisher id"
        self.publishers.add(publishers_id)

    def add_subscriber(subscriber_id, callback_function):
        if subscriber_id in self.subscribers:
            return "Need unique subscriber id"
        new_subscriber = self.redis_main.pubsub()
        while not new_subscriber.get_message():
            pass
        self.subscribers[subscriber_id] = {"redis_pubsub": new_subscriber,
                                           "callback_function": callback_function}

    def add_channel(channel_id):
        self.channels.add(channel_id)

    def add_subscription(subscriber_id, channel_id):
        callback_function = self.subscribers[subscriber_id]["callback_function"]
        self.subscribers[subscriber_id].subscribe(**{channel_id: callback_function})

    def publish(message, channel_id):
        self.redis_main(channel_id, message)

# how do you want to limit