class Pubsub: # how to map id to object?
    def __init__(self):
        self.publishers = dict()
        self.channels = dict()
        self.subscribers = dict()
        self.channel_to_subscriber = dict()

    def publisher_reg(self, publisher, id):
        self.publishers[id] = publisher
        #ligra.publisher(id)

    def channel_reg(self, channel, id):
        self.channels[id] = channel
        #ligra.channel(id)

    def subscriber_reg(self, subscriber, id):
        self.subscribers[id] = subscriber
        #ligra.subscriber(id)

    def subscribe(channel_id, subscriber_id):
        if channel_id in self.channel_to_subscriber:
            self.channel_to_subscriber[channel_id].append(subscriber_id)
        else:
            self.channel_to_subscriber[channel_id] = [subscriber_id]

        #ligra.subscribe(channel_id, subscriber_id)

class Publisher:
    def __init__(self):
        pass

class Channel:
    def __init__(self):
        pass

class Subscriber:
    def __init__(self):
        pass
