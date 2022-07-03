import pandas as pd
from src.utils import moora
import unittest

df, dx  = moora(2021)

class MooraTestMethods(unittest.TestCase):

    def test_instance(self):
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIsInstance(dx, pd.DataFrame)

    def test_result(self):
        self.assertTrue('Skor' in  df.columns.tolist())

    def test_number_of_criteria(self):
        self.assertEqual(len(dx.columns[4:]), 14)

if __name__ == '__main__':
    unittest.main()