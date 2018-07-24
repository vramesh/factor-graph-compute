import unittest
import edge

class EdgeTests(unittest.TestCase):
    def test(self):
        pass

suite = unittest.TestLoader().loadTestsFromTestCase(EdgeTests)
unittest.TextTestRunner(verbosity=2).run(suite)