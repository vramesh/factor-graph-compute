import redis
import time
from multiprocessing import Process, Manager, Array
import pdb
from threading import Thread
import pickle


class RedisBroker:
    def __init__(self):
        # self.redis_main = redis.StrictRedis(host='localhost',port=6379, db=0, decode_responses=True)
        self.redis_main = redis.Redis()
        self.redis_pubsub_object = self.redis_main.pubsub(ignore_subscribe_messages=True)
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
        new_subscriber = self.redis_pubsub_object
        self.subscribers[subscriber_id] = {"redis_pubsub": new_subscriber,
                                           "callback_function": callback_function}

    def add_channel(self,channel_id):
        self.channels.append(channel_id)

    def add_subscription(self,subscriber_id, channel_id):
        callback_function = self.subscribers[subscriber_id]["callback_function"]
        r = redis.Redis()
        self.subscribers[subscriber_id]["redis_pubsub"].subscribe(**{channel_id: callback_function})

    def decrypt(self, x):
        return str(x.decode("ascii")) if type(x) == bytes else x 

    def publish(self, channel_id, message):
        pickle_message = pickle.dumps(message)
        self.redis_main.publish(self.decrypt(channel_id), pickle_message)

    def start(self):
        def start_subscriber(subscriber_id):
            while True:
                message = self.subscribers[subscriber_id]["redis_pubsub"].get_message()
                if message is not None:
                    print("Got message! in " + subscriber_id + " " + str(message))
                # else:
                #     print("waiting")
                time.sleep(0.001)

        for subscriber_id in self.subscribers:
            process = Thread(target=start_subscriber,
                   args=(subscriber_id,))
            # process = Process(target=start_subscriber,
            #         args=(subscriber_id,))
            process.daemon = True
            process.start()














