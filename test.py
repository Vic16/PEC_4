import unittest
import pandas as pd
import re

from read_data import read_class_functions
from read_data import read_ORFs_data
from analytics import count_class
from analytics import mean_ORF_related
from analytics import ORFs_respiration
from analytics import count_class_multiplos


class TestDataExpl(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Loading dataset")
        path_file =  "data/tb_functions.pl"
        data = read_class_functions(path_file)
        cls._df = data
        cls.df_orf = read_ORFs_data(['data/orfs\\tb_data_00.txt',
                                        'data/orfs\\tb_data_01.txt',
                                        'data/orfs\\tb_data_02.txt',
                                        'data/orfs\\tb_data_03.txt',
                                        'data/orfs\\tb_data_04.txt',
                                        'data/orfs\\tb_data_05.txt'])
        cls.list_test = list(set(data["Ids"]))

    def test_ORFs_respiration(self):
        print("Starting test_ORFs_respiration")
        self.assertEqual(ORFs_respiration(self._df), 45)

    def test_count_class(self):
        print("Starting test_count_class")
        self.assertEqual(count_class(self._df, ".*hydro"), 166)
        self.assertEqual(count_class(self._df, ".*prot"), 311)
        self.assertEqual(count_class(self._df, ".*ca"), 83)
        self.assertEqual(count_class(self._df, ".*aci"), 28)

    def test_mean_ORF_related(self):
        print("Starting mean_ORF_related")
        self.assertEqual(mean_ORF_related(self._df, self.df_orf, ".*prot"), 32.73225806451613)
        self.assertEqual(mean_ORF_related(self._df, self.df_orf, ".*prot"), 37.04819277108434)
        self.assertEqual(mean_ORF_related(self._df, self.df_orf, ".*aci"), 33.464285714285715)

    def test_count_class_multiplos(self):
        print("Starting count_class_multiplos")
        self.assertEqual(count_class_multiplos(self.list_test, 2),117)
        self.assertEqual(count_class_multiplos(self.list_test, 3),59)
        self.assertEqual(count_class_multiplos(self.list_test, 4),43)
        self.assertEqual(count_class_multiplos(self.list_test, 5),666)
        self.assertEqual(count_class_multiplos(self.list_test, 6),16)
        self.assertEqual(count_class_multiplos(self.list_test, 7),19)
        self.assertEqual(count_class_multiplos(self.list_test, 8),7)


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestDataExpl))
unittest.TextTestRunner(verbosity=2).run(suite)
