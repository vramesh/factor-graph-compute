from state import NodeStateStore

class RedisCallbackClass:
    def __init__(self):
        pass

    def message_pass_wrapper_for_redis(incoming_message, input_function, pubsub):
        #is the callback functions for redis to run on pubsub
        #message format from redis: {'pattern': None, 'type': 'subscribe', 'channel': 'my-second-channel', 'data': 1L}
        
        node_id = incoming_message["channel"].decode("ascii").split("_")[1] #this is only redis dependent line
        updated_node_cache = RedisCallbackClass.update_node_cache(incoming_message, node_id)
        print(str(node_id) + " cache: "  + str(updated_node_cache))

        stop_countdown = NodeStateStore("redis").fetch_node(node_id,"stop_countdown")
        

        if stop_countdown > 0:
            for to_node_id in updated_node_cache:
                send_to_channel_name = node_id + "_" + to_node_id
                new_outgoing_message = RedisCallbackClass.compute_outgoing_message(input_function,updated_node_cache,node_id,to_node_id)
                RedisCallbackClass.propagate_message(send_to_channel_name, new_outgoing_message, pubsub)
                NodeStateStore("redis").countdown_by_one(node_id)
        else:
            print("terminated")

    def update_node_cache(incoming_message, node_id):
        updated_node_cache = NodeStateStore("redis").update_node(incoming_message, node_id)
        return updated_node_cache

    def compute_outgoing_message(input_function,updated_node_cache,from_node_id,to_node_id):
        node_data = NodeStateStore("redis").fetch_node(from_node_id,"node_data")
        new_outgoing_message = input_function(node_data, updated_node_cache,from_node_id,to_node_id)
        return new_outgoing_message

    def propagate_message(channel_name, new_outgoing_message, pubsub):
        pubsub.publish(channel_name, new_outgoing_message)
