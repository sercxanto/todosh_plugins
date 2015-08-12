#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""
    testlibtodotxt.py

    Unittests for libtodotxt.py, can be run by ./testlibtodo.py
"""
# The MIT License (MIT)
#
# Copyright (c) 2015 Georg Lutz <georg@georglutz.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime
import filecmp
import os
import unittest
import shutil
import tempfile
import libtodotxt


def check_agenda_data_equal(dict1, dict2):
    '''Tests if two agenda dicts contains the same entries, independend of the
    order.
    Returns True if dicts are equal, False otherwise
    '''
    
    if len(dict1) != len(dict2):
        return False

    for key1 in dict1:
        if key1 not in dict2:
            return False
        if sorted(dict2[key1]) != sorted(dict1[key1]):
            return False
    for key2 in dict2:
        if key2 not in dict1:
            return False
        if sorted(dict1[key2]) != sorted(dict2[key2]):
            return False

    return True


class TestReadTodoTxt(unittest.TestCase):
    '''unit tests for function readtodotxt()'''
    def setUp(self):
        script_dir = os.path.dirname(__file__)
        self.testdir = os.path.join(script_dir, "testfiles")

    def test_01(self):
        '''Simple todo.txt'''
        agenda_data = libtodotxt.readtodotxt(

        os.path.join(self.testdir, "todo01.txt"))
        expected = {None: [
            { "line": "Task1", "nr": 1  },
            { "line": "Task3", "nr": 3},
            { "line": "Task2", "nr": 2 },
            { "line": "Task4", "nr": 5 }]}
        self.assertTrue(check_agenda_data_equal(agenda_data, expected))

    def test_02(self):
        '''Simple todo.txt with one "t:"'''
        agenda_data = libtodotxt.readtodotxt(

        os.path.join(self.testdir, "todo02.txt"))
        expected = {
                None: [
                    { "line": "Task1", "nr": 1 },
                    { "line": "Task3", "nr": 3},
                    { "line": "Task4", "nr": 5 }],
                datetime.date(2015,01,01): [
                    { "line": "Task2 t:2015-01-01", "nr": 2 } ]}
        self.assertTrue(check_agenda_data_equal(agenda_data, expected))

    def test_03(self):
        '''Simple todo.txt with two "t:", one in the past'''
        agenda_data = libtodotxt.readtodotxt(
                os.path.join(self.testdir, "todo03.txt"))

        expected = {
                    None: [
                        { "line": "Task1", "nr": 1  },
                        { "line": "Task3", "nr": 3},
                        { "line": "Task4", "nr": 5 }],
                    datetime.date(2015,01,01): [
                        { "line": "Task2 t:2015-01-01", "nr": 2 } ],
                    datetime.date(2014,12,31): [
                        {"line": "Task5 t:2014-12-31", "nr": 7}]}
        self.assertTrue(check_agenda_data_equal(agenda_data, expected))

    def test_04(self):
        '''Date which cannot be parsed'''
        agenda_data = libtodotxt.readtodotxt(
            os.path.join(self.testdir, "todo04.txt"))
        expected = {
                    None: [
                        { "line": "Task1", "nr": 1 },
                        { "line": "Task3", "nr": 3 },
                        { "line": "Task4 t:abc", "nr": 5 }
                        , {"line": "Task6 t:", "nr":9}],
                    datetime.date(2015,01,01): [
                        { "line": "Task2 t:2015-01-01", "nr": 2 } ],
                    datetime.date(2014,12,31): [
                        {"line": "Task5 t:2014-12-31", "nr": 7}]}
        self.assertTrue(check_agenda_data_equal(agenda_data, expected))


class TestAddThresholdToEmpty(unittest.TestCase):
    '''unittests for function add_threshold_to_empty()'''
    def setUp(self):
        script_dir = os.path.dirname(__file__)
        self.testdir = os.path.join(script_dir, "testfiles")

    def test_01(self):
        '''Simple todo.txt'''
        now = datetime.date(2015, 01, 01)
        agenda_data = libtodotxt.readtodotxt(

        os.path.join(self.testdir, "todo01.txt"))
        libtodotxt.add_threshold_to_empty(agenda_data, now)
        expected = {
                    now: [
                        { "line": "Task1", "nr": 1  },
                        { "line": "Task3", "nr": 3 },
                        { "line": "Task2", "nr": 2 },
                        { "line": "Task4", "nr": 5 }]}
        self.assertTrue(check_agenda_data_equal(agenda_data, expected))

    def test_02(self):
        '''Simple todo.txt with one "t:"'''
        now = datetime.date(2015, 01, 01)
        agenda_data = libtodotxt.readtodotxt(

        os.path.join(self.testdir, "todo02.txt"))
        libtodotxt.add_threshold_to_empty(agenda_data, now)
        expected = {
                    now: [
                        { "line": "Task1", "nr": 1 },
                        { "line": "Task3", "nr": 3},
                        { "line": "Task2 t:2015-01-01", "nr": 2 },
                        { "line": "Task4", "nr": 5 }]}
        self.assertTrue(check_agenda_data_equal(agenda_data, expected))

    def test_03(self):
        '''Simple todo.txt with two "t:", one in the past'''
        now = datetime.date(2015, 01, 01)
        earlier = datetime.date(2014, 12, 31)
        agenda_data = libtodotxt.readtodotxt(

        os.path.join(self.testdir, "todo03.txt"))
        libtodotxt.add_threshold_to_empty(agenda_data, now)
        expected = {
                earlier: [
                    {"line": "Task5 t:2014-12-31", "nr":7 }],
                now: [
                    { "line": "Task1", "nr": 1  },
                    { "line": "Task3", "nr": 3},
                    { "line": "Task2 t:2015-01-01", "nr": 2 },
                    { "line": "Task4", "nr": 5 }]}
        self.assertTrue(check_agenda_data_equal(agenda_data, expected))

    def test_04(self):
        '''Date which cannot be parsed'''
        now = datetime.date(2015, 01, 01)
        earlier = datetime.date(2014, 12, 31)
        agenda_data = libtodotxt.readtodotxt(
            os.path.join(self.testdir, "todo04.txt"))
        libtodotxt.add_threshold_to_empty(agenda_data, now)
        expected = {
                earlier: [
                    {"line": "Task5 t:2014-12-31", "nr":7 }],
                now: [
                    { "line": "Task1", "nr": 1  },
                    { "line": "Task3", "nr": 3 },
                    { "line": "Task2 t:2015-01-01", "nr": 2 },
                    { "line": "Task4 t:abc", "nr": 5 },
                    {"line": "Task6 t:", "nr": 9}]}
        self.assertTrue(check_agenda_data_equal(agenda_data, expected))


class TestGetThresholdLineNr(unittest.TestCase):
    '''unit tests for function get_threshold_line_nr()'''
    def setUp(self):
        script_dir = os.path.dirname(__file__)
        self.testdir = os.path.join(script_dir, "testfiles")

    def test_01(self):
        '''nr_of_day=1'''
        now = datetime.date(2014, 12, 31)
        agenda_data = libtodotxt.readtodotxt(
            os.path.join(self.testdir, "todo05.txt"))
        actual = libtodotxt.get_threshold_line_nr(agenda_data, now, 1)
        expected = [1, 4]
        self.assertItemsEqual(expected, actual)

    def test_02(self):
        '''nr_of_day=2'''
        now = datetime.date(2014, 12, 31)
        agenda_data = libtodotxt.readtodotxt(
            os.path.join(self.testdir, "todo05.txt"))
        actual = libtodotxt.get_threshold_line_nr(agenda_data, now, 2)
        expected = [1, 4, 3]
        self.assertItemsEqual(expected, actual)

    def test_03(self):
        '''nr_of_day=3'''
        now = datetime.date(2014, 12, 31)
        agenda_data = libtodotxt.readtodotxt(
            os.path.join(self.testdir, "todo05.txt"))
        actual = libtodotxt.get_threshold_line_nr(agenda_data, now, 3)
        expected = [1, 4, 3, 2]
        self.assertItemsEqual(expected, actual)

    def test_04(self):
        '''threshold in future'''
        now = datetime.date(2014, 12, 28)
        agenda_data = libtodotxt.readtodotxt(
            os.path.join(self.testdir, "todo05.txt"))
        actual = libtodotxt.get_threshold_line_nr(agenda_data, now, 1)
        self.assertTrue(len(actual) == 0)

    def test_05(self):
        '''another now date, 1 matches'''
        now = datetime.date(2014, 12, 29)
        agenda_data = libtodotxt.readtodotxt(
            os.path.join(self.testdir, "todo05.txt"))
        actual = libtodotxt.get_threshold_line_nr(agenda_data, now, 2)
        expected = [4]
        self.assertItemsEqual(expected, actual)

    def test_06(self):
        '''date in between threshold entries'''
        now = datetime.date(2015, 01, 02)
        agenda_data = libtodotxt.readtodotxt(
            os.path.join(self.testdir, "todo05.txt"))
        actual = libtodotxt.get_threshold_line_nr(agenda_data, now, 10)
        expected = [1, 2, 3, 4]
        self.assertItemsEqual(expected, actual)

    def test_07(self):
        '''date at end of threshold entries'''
        now = datetime.date(2015, 01, 03)
        agenda_data = libtodotxt.readtodotxt(
            os.path.join(self.testdir, "todo05.txt"))
        actual = libtodotxt.get_threshold_line_nr(agenda_data, now, 10)
        expected = [1, 2, 3, 4]
        self.assertItemsEqual(expected, actual)

    def test_08(self):
        '''date in future'''
        now = datetime.date(2015, 01, 15)
        agenda_data = libtodotxt.readtodotxt(
            os.path.join(self.testdir, "todo05.txt"))
        actual = libtodotxt.get_threshold_line_nr(agenda_data, now, 10)
        expected = [1, 2, 3, 4]
        self.assertItemsEqual(expected, actual)

    def test_09(self):
        '''Ommited threshold'''
        now = datetime.date(2015, 01, 01)
        agenda_data = libtodotxt.readtodotxt(
            os.path.join(self.testdir, "todo06.txt"))
        libtodotxt.add_threshold_to_empty(agenda_data, now)
        actual = libtodotxt.get_threshold_line_nr(agenda_data, now, 10)
        expected = [1, 2, 3, 4]
        self.assertItemsEqual(expected, actual)


class TestMoveLines(unittest.TestCase):
    '''unit tests for function move_lines()'''
    def setUp(self):
        script_dir = os.path.dirname(__file__)
        self.testdir = os.path.join(script_dir, "testfiles")

    def start_testcase(self, testcase):
        '''Runs a testcase from the folder testfile/move_lines'''
        dirname = os.path.join(self.testdir, "move_lines", testcase)
        lines_filename = os.path.join(dirname, "lines.txt")
        from_before_filename = os.path.join(dirname, "from_before.txt")
        from_after_filename = os.path.join(dirname, "from_after.txt")
        from_after_preserve_filename = os.path.join(dirname, "from_after_preserve.txt")
        to_before_filename = os.path.join(dirname, "to_before.txt")
        to_after_filename = os.path.join(dirname, "to_after.txt")

        line_nrs = []
        with open(lines_filename) as file_:
            for line in file_:
                line_nrs.append(int(line))

        # Run with preserve flag, leaving empty lines
        temp_dir = tempfile.mkdtemp(prefix="tmp_testlibtodotxt")
        from_filename = os.path.join(temp_dir, "from.txt")
        to_filename = os.path.join(temp_dir, "to.txt")
        shutil.copyfile(from_before_filename, from_filename)
        shutil.copyfile(to_before_filename, to_filename)
        libtodotxt.move_lines(from_filename, to_filename, line_nrs, True)
        self.assertTrue(filecmp.cmp(
            from_filename, from_after_preserve_filename, shallow=False))
        self.assertTrue(filecmp.cmp(
            to_filename, to_after_filename, shallow=False))
        shutil.rmtree(temp_dir)

        # Runs without preserving line numbers, compact file
        temp_dir = tempfile.mkdtemp(prefix="tmp_testlibtodotxt")
        from_filename = os.path.join(temp_dir, "from.txt")
        to_filename = os.path.join(temp_dir, "to.txt")
        shutil.copyfile(from_before_filename, from_filename)
        shutil.copyfile(to_before_filename, to_filename)
        libtodotxt.move_lines(from_filename, to_filename, line_nrs, False)
        self.assertTrue(filecmp.cmp(
            from_filename, from_after_filename, shallow=False))
        self.assertTrue(filecmp.cmp(
            to_filename, to_after_filename, shallow=False))
        shutil.rmtree(temp_dir)

    def test_01(self):
        '''Empty to file'''
        self.start_testcase("01")

    def test_02(self):
        '''Empty from file'''
        self.start_testcase("02")

    def test_03(self):
        '''Simple move, non empty files'''
        self.start_testcase("03")

    def test_04(self):
        '''Empty lines'''
        self.start_testcase("04")

class TestGetKey(unittest.TestCase):
    '''unit tests for the function get_key()'''

    def test_01(self):
        '''Empty line'''
        line = ""
        actual = libtodotxt.get_key(line, "k")
        expected = None
        self.assertEqual(expected, actual)

    def test_02(self):
        '''Non-existing key'''
        line = "abcdefgh"
        actual = libtodotxt.get_key(line, "k")
        expected = None
        self.assertEqual(expected, actual)

    def test_03(self):
        '''Existing key at end'''
        line = "blah k:abcdef"
        actual = libtodotxt.get_key(line, "k")
        expected = "abcdef"
        self.assertEqual(expected, actual)

    def test_04(self):
        '''Existing key, followed by content'''
        line = "blah k:abcdef blub"
        actual = libtodotxt.get_key(line, "k")
        expected = "abcdef"
        self.assertEqual(expected, actual)

    def test_05(self):
        '''Existing key, followed by second key'''
        line = "blah k:abcdef k2:blub"
        actual = libtodotxt.get_key(line, "k")
        expected = "abcdef"
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()

