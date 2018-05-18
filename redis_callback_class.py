from state import NodeStateStore
import pickle

class RedisCallbackClass:
    def __init__(self):
        pass

    def message_pass_wrapper_for_redis(incoming_message, input_function, pubsub):
        #is the callback functions for redis to run on pubsub
        #message format from redis: {'pattern': None, 'type': 'subscribe', 'channel': 'my-second-channel', 'data': 1L}
        
        from_node_id = incoming_message["channel"].decode("ascii").split("_")[0] #this is only redis dependent line
        current_node_id = incoming_message["channel"].decode("ascii").split("_")[1] #this is only redis dependent line
        updated_node_cache, keep_publish = RedisCallbackClass.update_node_cache(incoming_message, current_node_id)
        
        print("Got message " + from_node_id + " " + current_node_id + " " + str(pickle.loads(incoming_message["data"])))
        if keep_publish:
            stop_countdown = NodeStateStore("redis").fetch_node(current_node_id,"stop_countdown")
            outgoing_neighbors = NodeStateStore("redis").fetch_node(current_node_id,"outgoing_neighbors")

            debug = False
            
            if stop_countdown > 0:
                # this is slightly inefficient implementation: should move for loop
                # to within the update_var / update_fac methods
                NodeStateStore("redis").countdown_by_one(current_node_id)

                for to_node_id in outgoing_neighbors:
                    if to_node_id[1:] != from_node_id[1:]:
                        send_to_channel_name = current_node_id + "_" + to_node_id
                        new_outgoing_message = \
                        RedisCallbackClass.compute_outgoing_message(input_function,updated_node_cache,
                            current_node_id,to_node_id,from_node_id)
                        RedisCallbackClass.propagate_message(send_to_channel_name, new_outgoing_message, pubsub)
            elif stop_countdown == 0:
                print("terminated")

    def update_node_cache(incoming_message, node_id):
        modified_incoming_message = dict()
        modified_incoming_message["channel"] = incoming_message["channel"].decode('ascii')
        modified_incoming_message["data"] = pickle.loads(incoming_message["data"])
        
        if modified_incoming_message["data"] is None:
            return updated_node_cache, False
        else:
            updated_node_cache = NodeStateStore("redis").update_node(modified_incoming_message, node_id)
            return updated_node_cache, True

    def compute_outgoing_message(input_function,updated_node_cache,current_node_id,to_node_id,from_node_id):
        node_data = NodeStateStore("redis").fetch_node(current_node_id,"node_data")
        new_outgoing_message = \
        input_function(node_data,updated_node_cache,current_node_id,to_node_id, from_node_id)
        return new_outgoing_message

    def propagate_message(channel_name, new_outgoing_message, pubsub):
        if new_outgoing_message is not None:
            pubsub.publish(channel_name, new_outgoing_message)
