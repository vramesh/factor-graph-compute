class PubSub: # how to map id to object?
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

class Publisher:
    def __init__(self, node_id):
        pass

    def publish(self):
        pass

    def register(self):
        pass



class Channel:
    def __init__(self):
        pass

    def register(self):
        pass


class Subscriber:
    def __init__(self, node_id):
        self.callback_function = None

    def subscribe(self):
        pass

    def register(self, callback_function):
        self.callback_function = callback_function
