import unittest
from tests import test_event


def main():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromModule(test_event))

    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    main()