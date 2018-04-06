import redis
import time
from multiprocessing import Process, Manager, Array

class RedisBroker:
    def __init__(self):
        # self.redis_main = redis.StrictRedis(host='localhost',port=6379, db=0, decode_responses=True)
        self.redis_main = redis.Redis()
        self.publishers = set()
        self.channels = list()
        self.subscribers = dict()

    def add_publisher(self,publisher_id):
        if publisher_id in self.publishers:
            return "Need unique publisher id"
        self.publishers.add(publisher_id)

    def add_subscriber(self,subscriber_id, callback_function):
        if subscriber_id in self.subscribers:
            return "Need unique subscriber id"
        new_subscriber = self.redis_main.pubsub(ignore_subscribe_messages=True)
        self.subscribers[subscriber_id] = {"redis_pubsub": new_subscriber,
                                           "callback_function": callback_function}

    def add_channel(self,channel_id):
        self.channels.append(channel_id)

    def add_subscription(self,subscriber_id, channel_id):
        callback_function = self.subscribers[subscriber_id]["callback_function"]
        self.subscribers[subscriber_id]["redis_pubsub"].subscribe(**{channel_id: callback_function})

    def publish(self, channel_id, message):
        self.redis_main.publish(channel_id, message)

    def start(self):
        def start_subscriber(subscriber_id):
            while True:
                message = self.subscribers[subscriber_id]["redis_pubsub"].get_message()
                if message:
                    print("Got message! in " + subscriber_id + str(message))
                # else:
                #     print("waiting")
                time.sleep(0.01)

        for subscriber_id in self.subscribers:
            process = Process(target=start_subscriber,
                    args=(subscriber_id,))
            process.daemon = True
            process.start()


def test_pubsub_redis():
    redis = RedisBroker()
    redis.add_publisher("p1")
    redis.add_publisher("p2")
    redis.add_subscriber("s1",lambda x: print("hello"))
    redis.add_subscriber("s2",lambda x: print("bye"))
    redis.add_subscription("s1","c789")
    redis.add_subscription("s2","c789")
    redis.start()
    time.sleep(0.1)
    redis.publish("first_try","c789")
    redis.publish("first_try","c789")
    redis.publish("first_try","c789")
    redis.publish("first_try","c789")
    redis.publish("first_try","c789")














