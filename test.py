import unittest
from daycountconventions import conventions
from datetime import datetime


class DayCountConventionTestCase(unittest.TestCase):

    def setUp(self):
        self.test_data = []
        self.test_data.append((datetime.strptime('2017-01-15', '%Y-%m-%d'), datetime.strptime('2017-03-31', '%Y-%m-%d')))
        self.test_data.append((datetime.strptime('2017-01-31', '%Y-%m-%d'), datetime.strptime('2017-03-31', '%Y-%m-%d')))
        self.test_data.append((datetime.strptime('2017-01-31', '%Y-%m-%d'), datetime.strptime('2017-02-28', '%Y-%m-%d')))

    def tearDown(self):
        pass

    def test_DCC30360(self):
        result = [76. / 360., 60. / 360., 28. / 360.]
        for idx, date_tuple in enumerate(self.test_data):
            conv = conventions.DCC30360(date_tuple[0], date_tuple[1])
            self.assertAlmostEqual(conv.accrual_factor, result[idx], places=5)

    def test_DCC30E360(self):
        result = [75. / 360., 60. / 360., 28. / 360.]
        for idx, date_tuple in enumerate(self.test_data):
            conv = conventions.DCC30E360(date_tuple[0], date_tuple[1])
            self.assertAlmostEqual(conv.accrual_factor, result[idx], places=5)

    def test_DCC30E360ISDA(self):
        termination_date = datetime.strptime('2017-04-01', '%Y-%m-%d')
        result = [75. / 360., 60. / 360., 30. / 360.]
        for idx, date_tuple in enumerate(self.test_data):
            conv = conventions.DCC30E360ISDA(date_tuple[0], date_tuple[1], termination_date)
            self.assertAlmostEqual(conv.accrual_factor, result[idx], places=5)

    def test_DCC30EP360ISDA(self):
        result = [76. / 360., 61. / 360., 28. / 360.]
        for idx, date_tuple in enumerate(self.test_data):
            conv = conventions.DCC30EP360ISDA(date_tuple[0], date_tuple[1])
            self.assertAlmostEqual(conv.accrual_factor, result[idx], places=5)

if __name__ == '__main__':
    dcc_suite = unittest.TestLoader().loadTestsFromTestCase(DayCountConventionTestCase)
    all_suite = unittest.TestSuite([dcc_suite])
    unittest.TextTestRunner(verbosity=2).run(all_suite)
