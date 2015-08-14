# vim: set fileencoding=utf-8 :
"""
    libtodotxt.py

    Library with common functions to todo.txt addons

    This is no complete implementation of the todo.txt format.
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
import os
import re
import tempfile


def get_key_search_pattern(key):
    '''Returns the re search pattern for a given key'''
    return "(^|(?P<spaces>\s))" + key + ":" + "(?P<value>\\S+)"


def get_key(line, key):
    '''
    Returns a value referenced by key from a todo line (first occurence).
    Returns None if key is not found
    '''
    pattern = get_key_search_pattern(key)
    result = re.search(pattern, line)
    if result != None:
        return result.group("value")
    return None


def set_key(line, key, value):
    '''
    Sets or adds (if not existent) a key inside the line to a value. If value
    is None, the key is deleted completely.
    Returns the changed line.
    '''
    search_pattern = get_key_search_pattern(key)
    replace_pattern = ""
    if value is not None:
        replace_pattern = "\\g<spaces>" + key + ":" + value

    (new_line, number_of_subs_made) = re.subn(
            search_pattern, replace_pattern, line)
    if number_of_subs_made == 0 and value is not None:
        if len(line) > 0:
            new_line = line + " "
        new_line = new_line + key + ":" + value
    return new_line


def add_interval(date_str, interval):
    '''
    Adds an interval to an iso8601 date and returns the result

    Parameters:

    - date: date string in ISO8601 format: "2015-01-01"
    - interval: textual representation of an time interval: number + qualifier,
    e.g. "1y". Valid qualifiers are
        - "y": year
        - "m": month
        - "w": week
        - "d": day
    '''
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    pattern = "(?P<number>\d+)(?P<qual>[ymwd])"
    result = re.search(pattern, interval)

    if result is None:
        return None

    number = int(result.group("number"))
    qual = result.group("qual")

    delta = None
    nr_days = 0

    if qual == "y":
        nr_days = number * 365
    elif qual == "m":
        nr_days = number * 30
    elif qual == "w":
        nr_days = number * 7
    elif qual == "d":
        nr_days = number
    delta = datetime.timedelta(days = nr_days)

    final_date = date + delta
    return final_date.strftime("%Y-%m-%d")


def add_recur(from_filename, to_filename, max_threshold, is_dryrun):
    '''
    Adds recurring tasks from from_filename to to_filename.
    A single repeating task may be added several times, depending on how many
    intervals fit in the timeframe until max_threshold is reached.
    In to_filename the "rec:" tag is stripped, in from_filename the "t:"
    tag is changed to the date of the next recurrence (the first one later as
    max_threshold).

    Parameters:
        - max_threshold: maximum threshold date in ISO 8601 text format
        - is_dryrun: Do not change file, only return changed lines
    Returns:
        Dictionary with information with new/updated lines in to/from file, e.g.:
        { "from": [
            "Task1 t:2015-07-15 rec:2w",
            "Task2 t:2015-07-22 rec:1m"
            ],
          "to": [
            "Task1 t:2015-07-01",
            "Task2 t:2015-06-22"
            ]
        }
    '''

    result = {}
    result["from"] = []
    result["to"] = []

    from_file = open(from_filename, "r")

    if not is_dryrun:
        new_from_file = tempfile.NamedTemporaryFile(mode="a",
                dir=os.path.dirname(from_filename), delete=False)
        new_from_filename = new_from_file.name

    if not is_dryrun:
        to_file = open(to_filename, "a")

    for line in from_file:
        rec = get_key(line, "rec")
        threshold = get_key(line, "t")
        old_threshold = threshold
        if rec != None and threshold != None:
            # string comparison, works with ISO8601
            while threshold <= max_threshold:
                line_to_file = set_key(line, "rec", None)
                line_to_file = set_key(line_to_file, "t", threshold)
                if not is_dryrun:
                    to_file.write(line_to_file)
                result["to"].append(line_to_file.strip())
                threshold = add_interval(threshold, rec)
        line_from_file = set_key(line, "t", threshold)
        if not is_dryrun:
            new_from_file.write(line_from_file)
        if old_threshold != threshold:
            result["from"].append(line_from_file.strip())

    from_file.close()
    if not is_dryrun:
        new_from_file.close()
        to_file.close()
        os.remove(from_filename)
        os.rename(new_from_filename, from_filename)

    return result


def move_lines(from_filename, to_filename, line_nrs, preserve_line_nrs):
    '''
    Copies the lines referenced in the list line_nrs from from_filename to
    to_filename and deletes empty lines in from_filename
    If preserve_line_nrs is set to True, then the moved lines in from_file
    are replaced by empty lines. If preserve_line_nrs is set to False they are
    removed completely, so the line numbers are changing.'''

    new_from_file = tempfile.NamedTemporaryFile(mode="a",
            dir=os.path.dirname(from_filename), delete=False)
    new_from_filename = new_from_file.name

    from_file = open(from_filename, "r")
    to_file = open(to_filename, "a")

    for line_nr, line in enumerate(from_file, start=1):
        if line_nr in line_nrs:
            if preserve_line_nrs:
                new_from_file.write("\n")
            to_file.write(line)
        else:
            new_from_file.write(line)
    to_file.close()
    from_file.close()
    new_from_file.close()

    os.remove(from_filename)
    os.rename(new_from_filename, from_filename)



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

