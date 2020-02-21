import unittest
import os, sys, inspect
from src.solr_import import file_len

import os

dir_path = os.path.dirname(os.path.realpath(__file__))
resource_path = dir_path + os.sep + "resources"


class solr_import_test(unittest.TestCase):
    def test_file_len(self):
        file = resource_path + "/testfilelen.txt"
        len = file_len(file)
        self.assertEqual(5, len)


if __name__ == "__main__":

    unittest.main()
