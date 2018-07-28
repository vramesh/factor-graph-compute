import unittest
import state

class StateTests(unittest.TestCase):
    def test(self):
        pass

suite = unittest.TestLoader().loadTestsFromTestCase(StateTests)
unittest.TextTestRunner(verbosity=2).run(suite)