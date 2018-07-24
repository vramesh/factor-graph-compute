import unittest
import mock
from factor_graph import FactorGraph, FactorGraphService, Node, Edge 

class TestFactorGraph(unittest.TestCase):
    pass

class TestFactorGraphService(unittest.TestCase):
    ## mock FG for failure tests
    def test_create_success(self):
        factor_graph_service = FactorGraphService()
        factor_graph = factor_graph_service.create('some path')
        self.assertIsInstance(factor_graph, FactorGraph)

    def test_run_success(self):
        factor_graph_service = FactorGraphService()
        factor_graph = factor_graph_service.create('some path')
        result = factor_graph_service.run(factor_graph)
        self.assertIsInstance(result, dict)

class TestEdge(unittest.TestCase):
    pass

class TestNode(unittest.TestCase):
    @mock.patch('state.NodeState')
    def setUp(self, mock_node_state):
        node_id = 0
        node_function = lambda x, y: x + y

        self.node_state = mock_node_state.return_value
        self.node = Node(node_id, node_function, self.node_state)

    def test_message_pass_success(self):
        incoming_message = 'incoming'
        self.assertIsNone(self.node.message_pass(incoming_message))

    def test_message_pass_update_state_exception(self):
        self.node_state.update.side_effect = Exception()
        incoming_message = 'incoming'
        self.assertRaises(Exception, self.node.message_pass, incoming_message)

    def test_message_pass_compute_outgoing_message_exception(self):
        pass

    @mock.patch('Pubsub.Publisher.publish')
    def test_message_pass_propagate_message_exception(self, mock_publish_call):
        mock_publish_call.side_effect = Exception()
        incoming_message = 'incoming'
        self.assertRaises(Exception, self.node.message_pass, incoming_message)


if __name__ == '__main__':
    unittest.main()
