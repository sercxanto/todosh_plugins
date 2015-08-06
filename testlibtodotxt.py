#!/usr/bin/env python

import datetime
import os
import unittest
import libtodotxt


def testAgendaDataEqual(dict1, dict2):
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
    def setUp(self):
        scriptDir = os.path.dirname(__file__)
        self.testdir = os.path.join(scriptDir, "testfiles")

    def test_01(self):
        '''Simple todo.txt'''
        now = datetime.date(2015,01,01)
        agenda_data = libtodotxt.readtodotxt(

            os.path.join(self.testdir, "todo01.txt"), now)
        expected = {now: [ { "line": "Task1", "nr": 1  }, { "line": "Task3", "nr": 3}, { "line": "Task2", "nr": 2 }, { "line": "Task4", "nr": 5 }]}
        self.assertTrue(testAgendaDataEqual(agenda_data, expected))



if __name__ == '__main__':
    unittest.main()

