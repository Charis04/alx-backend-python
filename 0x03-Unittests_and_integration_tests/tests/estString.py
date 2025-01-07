import unittest


class TestStrings(unittest.TestCase):
    """Tests string methods"""

    def setUp(self):
        self.s = "my name"

    @unittest.expectedFailure
    def test_split(self):
        self.assertEqual(self.s.split(), ['my', 'names'], 'they are not equal')

    def test_error(self):
        with self.assertRaises(TypeError):
            self.s.split(2)


if __name__ == '__main__':
    unittest.main()
