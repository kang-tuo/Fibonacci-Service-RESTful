import unittest
from generator import Generator


class TestCentralData(unittest.TestCase):

    def test_if_generate_correct(self):
        input_number = 11
        generator = Generator()
        combinations = generator.generate_combinations(input_number)
        expected = [[8, 3], [5, 3, 3], [3, 2, 3, 3], [5, 2, 2, 2], [3, 2, 2, 2, 2]]
        self.assertEqual(expected, combinations)


def create_suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestCentralData())
    return test_suite


if __name__ == '__main__':
    suite = create_suite()
    runner = unittest.TextTestRunner()
    runner.run(suite)
