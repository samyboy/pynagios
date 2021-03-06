#!/usr/bin/env python

import unittest
import sys


import pynagios


class ReadmeExamples(unittest.TestCase):

    def test_example1(self):

        # 2a. create the first service
        service1 = pynagios.Service("Service1")
        service1.value = 23
        service1.max_level = 100
        service1.warn_level = 85
        service1.crit_level = 95

        # 3. create a "Check" instance
        check = pynagios.Check()

        # 5. add the services into the nagios instance
        check.add(service1)

        # 5. print the check
        print check.output()

        # 6. exit with the appropriate exit code
        self.assertEqual(check.exit_code, 0)


class SimpleServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.check = pynagios.Check()
        self.service = pynagios.Service('single_service')
        self.service.max_level = 100


class Test_Exceptions(SimpleServiceTestCase):

    def setUp(self):
        super(Test_Exceptions, self).setUp()

    def test_no_service(self):
        with self.assertRaises(Exception):
            self.check.output()

    def test_mix_abs_percent(self):
        self.service.warn_level = '80'
        self.service.crit_level = '90%'
        with self.assertRaises(Exception):
            self.check.add(self.service)

    def test_mix_percent_abs(self):
        self.service = warn_level = '50%'
        self.service = crit_level = '60'
        with self.assertRaises(Exception):
            self.check.add(self.service)

class Absolute_Values_TestCase(SimpleServiceTestCase):

    def setUp(self):
        super(Absolute_Values_TestCase, self).setUp()
        self.service.warn_level = 80
        self.service.crit_level = 90

    def test_check_ok(self):
        self.service.value = 1
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'OK')
        self.assertEqual(self.check.exit_code, 0)
        self.assertEqual(self.check.output(), 'OK - single_service is OK 1/100')

    def test_check_warning(self):
        self.service.value = 81
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'WARNING')
        self.assertEqual(self.check.exit_code, 1)
        self.assertEqual(self.check.output(), 'WARNING - single_service is WARNING 81/100')

    def test_check_critical(self):
        self.service.value = 91
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'CRITICAL')
        self.assertEqual(self.check.exit_code, 2)
        self.assertEqual(self.check.output(), 'CRITICAL - single_service is CRITICAL 91/100')

    def test_no_value(self):
        self.service.value = None
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'UNKNOWN')
        self.assertEqual(self.check.exit_code, 3)
        self.assertEqual(self.check.output(), 'UNKNOWN - single_service is UNKNOWN None/100')


class Percent_Values_TestCase(SimpleServiceTestCase):

    def setUp(self):
        super(Percent_Values_TestCase, self).setUp()
        self.service.warn_level = '80%'
        self.service.crit_level = '90%'

    def test_check_ok(self):
        self.service.value = 1
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'OK')
        self.assertEqual(self.check.exit_code, 0)
        self.assertEqual(self.check.output(), 'OK - single_service is OK 1/100')

    def test_check_warning(self):
        self.service.value = 85
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'WARNING')
        self.assertEqual(self.check.exit_code, 1)
        self.assertEqual(self.check.output(), 'WARNING - single_service is WARNING 85/100')

    def test_check_critical(self):
        self.service.value = 95
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'CRITICAL')
        self.assertEqual(self.check.exit_code, 2)
        self.assertEqual(self.check.output(), 'CRITICAL - single_service is CRITICAL 95/100')


    def test_check_unknown(self):
        self.service.value = None
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'UNKNOWN')
        self.assertEqual(self.check.exit_code, 3)
        self.assertEqual(self.check.output(), 'UNKNOWN - single_service is UNKNOWN None/100')



class No_Max_Value_TestCase(unittest.TestCase):
    def setUp(self):
        self.check = pynagios.Check()
        self.service = pynagios.Service('no_max_value')
        self.service.warn_level = 80
        self.service.crit_level = 90

    def test_check_ok(self):
        self.service.value = 10
        self.service.text = '%(name)s has value of %(value)s'
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'OK')

    def test_check_warning(self):
        self.service.value = 81
        self.service.text = '%(name)s has value of %(value)s'
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'WARNING')

    def test_check_critical(self):
        self.service.value = 91
        self.service.text = '%(name)s has value of %(value)s'
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'CRITICAL')

class Exit_Code_TestCase(SimpleServiceTestCase):

    def test_exit_codes(self):
        self.assertEqual(self.check.status_codes['OK'], 0)
        self.assertEqual(self.check.status_codes['WARNING'], 1)
        self.assertEqual(self.check.status_codes['CRITICAL'], 2)
        self.assertEqual(self.check.status_codes['UNKNOWN'], 3)


class StringServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.service = pynagios.Service('single_service')
        self.service.stringvalues = True
        self.service.ok_level = 'ok'
        self.service.warn_level = 'warn'
        self.service.crit_level = 'crit'
        self.check = pynagios.Check()

class String_Values_TestCase(StringServiceTestCase):

    def test_ok_all_defined(self):
        self.service.value = 'ok'
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'OK')

    def test_critical_all_defined(self):
        self.service.value = 'crit'
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'CRITICAL')

    def test_warning_all_defined(self):
        self.service.value = 'warn'
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'WARNING')

    def test_unknown_all_defined(self):
        self.service.value = 'other'
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'UNKNOWN')
        self.assertEqual(self.check.exit_code, 3)

    def test_check_ok_exclude_ok(self):
        self.service.value = 'ok'
        self.service.ok_level = None
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'OK')

    def test_check_ok_exclude_warning(self):
        self.service.value = 'ok'
        self.service.warn_level = None
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'OK')

    def test_check_ok_exclude_critical(self):
        self.service.value = 'ok'
        self.service.crit_level = None
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'OK')

    def test_check_warning_exclude_ok(self):
        self.service.value = 'warn'
        self.service.ok_level = None
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'WARNING')

    def test_check_warning_exclude_warning(self):
        self.service.value = 'warn'
        self.service.warn_level = None
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'WARNING')

    def test_check_warning_exclude_critical(self):
        self.service.value = 'warn'
        self.service.crit_level = None
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'WARNING')

    def test_check_critical_exclude_ok(self):
        self.service.value = 'crit'
        self.service.ok_level = None
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'CRITICAL')

    def test_check_critical_exclude_warning(self):
        self.service.value = 'crit'
        self.service.warn_level = None
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'CRITICAL')

    def test_check_critical_exclude_critical(self):
        self.service.value = 'crit'
        self.service.crit_level = None
        self.check.add(self.service)
        self.assertEqual(self.check.status, 'CRITICAL')



if __name__ == "__main__":
    unittest.main(verbosity=2)
