import unittest
import factor_graph

class FactorGraphTests(unittest.TestCase):
    def test(self):
        pass

suite = unittest.TestLoader().loadTestsFromTestCase(FactorGraphTests)
unittest.TextTestRunner(verbosity=2).run(suite)