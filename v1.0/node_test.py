import unittest
import node

class NodeTests(unittest.TestCase):
    def test(self):
        self.assertEqual(node.Node().add(4,5),9)

suite = unittest.TestLoader().loadTestsFromTestCase(NodeTests)
unittest.TextTestRunner(verbosity=2).run(suite)