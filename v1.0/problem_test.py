import unittest
import problem

class ProblemTests(unittest.TestCase):
    def test(self):
        self.assertEqual(node.Node().add(4,5),9)

suite = unittest.TestLoader().loadTestsFromTestCase(ProblemTests)
unittest.TextTestRunner(verbosity=2).run(suite)