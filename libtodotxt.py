
import datetime
import re


def move_lines(from_file, to_file, line_nrs, preserve_line_nrs):
    '''
    Copies the lines referenced in the list line_nrs from from_file to
    to_file and deletes empty lines in from_file
    If preserve_line_nrs is set to True, then the moved lines in from_file
    are replaced by empty lines. If preserve_line_nrs is set to False they are
    removed completely, so the line numbers are changing.'''
    # TODO implement
    pass


def add_threshold_to_empty(agenda_data, threshold):
    '''
    Adds the given threshold value (datetime.date object) to entries with no
    threshold (key is None).
    '''
    if None in agenda_data:
        if threshold not in agenda_data:
            agenda_data[threshold] = []
        agenda_data[threshold].extend(agenda_data[None])
        del agenda_data[None]


def get_threshold_line_nr(agenda_data, now, nr_of_days):
    '''Returns a list of line_numbers of filtered agenda_data
    contains tasks either overdue or due in next nr_of_days days
    '''
    limit = now + datetime.timedelta(days=nr_of_days)
    result = []
    for date in agenda_data:
        if date <= limit:
            for entry in agenda_data[date]:
                result.append(entry["nr"])
    return result


def getthreshold(line):
    '''Parses line and returns threshold ("t:") date object
    python date objects are comparable to each other
    If the date cannot be parsed (because the format does not match or
    threshold date is not available) None is returned.
    '''
    pattern = " t:(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})"
    result = re.search(pattern, line)
    if result != None:
        return datetime.date(int(result.group("year")),
                int(result.group("month")),
                int(result.group("day")))
    else:
        return None


def readtodotxt(todo_filename):
    '''Reads the todo.txt file and returns the following dict (example):

        { 2015-01-01:
            [ { "line": "(B) Task1", "nr": 5 }, { "line": "(A) Task2", "nr": 4 }, { "line": "Task3", "nr": 1 } ],
          2015-01-02:
            [ { "line": "Task4", "nr": 3} , {"line": "(C) Task5", "nr": 2}, {"line": "(A) Task6", "nr": 6 } ]
        }

        - The date is a datetime.date object
        - The numbers are line numbers

    '''
    agenda_data = {}
    todo_file = open(todo_filename, "r")
    line_nr = 1
    for line in todo_file:
        line = line.rstrip()
        # Skip over empty lines
        if len(line) > 0:
            threshold = getthreshold(line)
            if not threshold in agenda_data:
                agenda_data[threshold] = []
            item = {}
            item["line"] = line
            item["nr"] = line_nr
            agenda_data[threshold].append(item)
        line_nr = line_nr + 1
    todo_file.close()

    return agenda_data

