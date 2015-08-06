
import datetime
import re


def getthreshold(line, defaultdate):
    '''Parses line and returns threshold ("t:") date object
    python date objects are comparable to each other
    If the date cannot be parsed (because the format does not match or
    threshold date is not available) the current date is returned.
    '''
    pattern = " t:(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})"
    result = re.search(pattern, line)
    if result != None:
        return datetime.date(int(result.group("year")),
                int(result.group("month")),
                int(result.group("day")))
    else:
        return defaultdate


def readtodotxt(todo_filename, now):
    '''Reads the todo.txt file and returns the following dict (example):

        { 2015-01-01:
            [ { "line": "(B) Task1", "nr": 5 }, { "line": "(A) Task2", "nr": 4 }, { "line": "Task3", "nr": 1 } ],
          2015-01-02:
            [ { "line": "Task4", "nr": 3} , {"line": "(C) Task5", "nr": 2}, {"line": "(A) Task6", "nr": 6 } ]
        }

        - The date is a datetime.date object
        - The numbers are line numbers

    Parameters:
        now: datetime.timestamp considered to be "now"
    '''
    agenda_data = {}
    todo_file = open(todo_filename, "r")
    line_nr = 1
    for line in todo_file:
        line = line.rstrip()
        # Skip over empty lines
        if len(line) > 0:
            threshold = getthreshold(line, now)
            if not threshold in agenda_data:
                agenda_data[threshold] = []
            item = {}
            item["line"] = line
            item["nr"] = line_nr
            agenda_data[threshold].append(item)
        line_nr = line_nr + 1
    todo_file.close()

    return agenda_data

