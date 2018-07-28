from redis_callback_class import *
from state import RedisNodeStateStore
from node_update_functions import ALGORITHM_TO_UPDATE_FUNCTIONS
from redis import Redis
import timeit
from Pubsub import PubSub

def timer(function_to_time):
    def function_timer(*args, **kwargs):
        setup()
        t = timeit.Timer(function_to_time)
        time_to_run = t.timeit(10)
        takedown()
        print(function_to_time.__name__, " benchmark: ", time_to_run)
    return function_timer

def setup():
    redis.flushall()

    node_cache = RedisNodeStateStore()
    node_cache.create_node_state(node_id, initial_messages, node_type,
            node_data, stop_countdown)

def takedown():
    redis.flushall()

@timer
def profile_message_pass():
    RedisCallbackClass.message_pass_wrapper_for_redis(incoming_message,
            input_function, pubsub)

@timer
def profile_update_node_cache():
    RedisCallbackClass.update_node_cache(incoming_message, node_id)

@timer
def profile_compute_outgoing_message():
    neighbor_node_messages = {'v0': 0.5}
    to_node_id = 'v0' 
    RedisCallbackClass.compute_outgoing_message(input_function,
            neighbor_node_messages, node_id, to_node_id)


if __name__ == '__main__':

    redis = Redis()
    incoming_message = {'channel': 'v0_f0'.encode('ascii'), 'data': '0.5'}
    input_function = ALGORITHM_TO_UPDATE_FUNCTIONS['test']['update_fac']
    pubsub = PubSub('redis')

    node_id = 'f0'
    node_type = 'factor'
    initial_messages = {'v0': 0} 
    node_data = 0
    stop_countdown = 99999999 

    profile_message_pass()
    profile_update_node_cache()
    profile_compute_outgoing_message()
