import unittest
import os, sys, inspect, json
from src.solr_export import prep_url, exclude, match

dir_path = os.path.dirname(os.path.realpath(__file__))
resource_path = dir_path + os.sep + "resources"


class solr_export_test(unittest.TestCase):
    def test_prep_url(self):
        preped = prep_url("http://localhost:8983", {"q": "fish", "sort": "id asc"})
        self.assertEqual(preped, "http://localhost:8983/select?q=fish&sort=id+asc")

    def test_exclude(self):
        with open(resource_path + "/doc_testexclude.json") as doc:
            json_doc = json.load(doc)

            # test basic exclude
            excluded = exclude(json_doc, "*_sort")
            self.assertEqual(
                excluded,
                {"id": "test", "sort_key": "value", "title_search": "title_value"},
            )

            # test comma separated exclude
            excluded = exclude(json_doc, "*_sort,*_search")
            self.assertEqual(excluded, {"id": "test", "sort_key": "value"})

            # test multiple exclude
            json_doc = {"id": "1", "fish_exclude": "ex1", "other_exclude": "ex2"}
            excluded = exclude(json_doc, "*_exclude")
            self.assertEqual(excluded, {"id": "1"})

    def test_match(self):
        self.assertTrue(match("title_search", "*_search"))
        self.assertTrue(match("sort_key", "sort_*"))
        self.assertTrue(match("title_search", "*_search,sort_*"))

if __name__ == "__main__":

    unittest.main()
