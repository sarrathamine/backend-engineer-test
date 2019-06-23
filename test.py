import unittest
import os
import json
from datetime import datetime
from exercise import get_months
from exercise import in_between
from exercise import process_data
from exercise import write_result

class TestExercise(unittest.TestCase):

    def test_get_months(self):
        res = get_months((datetime(2016,1,1), datetime(2016, 2,1)))
        self.assertEqual(res, 1)
    def test_in_between(self):
        res = in_between(datetime(2016,2,1), datetime(2016,1,1), datetime(2016, 3,1))
        self.assertTrue(res)
        res = in_between(datetime(2016,12,1), datetime(2016,1,1), datetime(2016, 3,1))
        self.assertFalse(res)
    def test_process_data(self):
        # first case empty dict
        result = process_data({"freelance": {}})
        self.assertEqual(result, {})

        # second case with id and no professionalExperiences
        freelancerFile = './test/freelancer0.json'
        if not os.path.isfile(freelancerFile):
            print("File does not exists")

        with open(freelancerFile) as f:
            data = json.load(f)
        result = process_data(data)
        self.assertIsNotNone(result["freelance"]["id"])
        self.assertEqual(result["freelance"]["computed_skills"], [])

        # third case with professionalExperiences
        freelancerFile = './test/freelancer.json'
        if not os.path.isfile(freelancerFile):
            print("File does not exists")

        with open(freelancerFile) as f:
            data = json.load(f)
        result = process_data(data)
        self.assertIsNotNone(result["freelance"]["id"])
        self.assertNotEqual(result["freelance"]["computed_skills"], [])
    def test_write_result(self):
        res_path = "./test/result_test.json"
        write_result({"test": "test"}, res_path)
        self.assertTrue(os.path.isfile(res_path))
        with open(res_path) as f:
            data = json.load(f)
        self.assertEqual(data, {"test": "test"})
        
if __name__ == '__main__':
    unittest.main()
