#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""
    agenda.py

    Prints overview of scheduled tasks in todo.txt (plugin for todo.sh)
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
from __future__ import print_function
import argparse
import datetime
import os
import re
import sys

# Name of the plugin (shell wrapper script)
PLUGIN_NAME = "agenda"

def usage(args):
    '''Usage message for todo.sh plugin system'''
    print("    " + PLUGIN_NAME + ": " + "Prints overview of scheduled ('t:') task for next 10 days")
    print("      Non-scheduled tasks are printed under the current date")


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



def plugin(args):
    '''Plugin main logic'''

    todo_dir = os.environ.get("TODO_DIR")
    if todo_dir == None:
        print("Env variable TODO_DIR not set! Exit.", file=sys.stderr)
        sys.exit(1)

    todo_filename = os.path.join(todo_dir, "todo.txt")

    if not os.path.isfile(todo_filename):
        print("todo.txt not found in TODO_DIR! Exit.", file=sys.stderr)
        sys.exit(1)

    now = datetime.date.today()
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
            agenda_data[threshold].append(line)
        line_nr = line_nr + 1
    todo_file.close()

    for key in agenda_data:
        agenda_data[key].sort()
    
    for key in sorted(agenda_data):
        datestring = key.strftime("%a, %Y-%m-%d")
        print(datestring)
        print("-" * len(datestring))
        print()
        for entry in agenda_data[key]:
            print(entry)
        print()
        print()



def main():
    '''main function'''
    parser = argparse.ArgumentParser(prog=PLUGIN_NAME)
    subparsers = parser.add_subparsers()
    parser_usage = subparsers.add_parser('usage', help='show usage message')
    parser_usage.set_defaults(func=usage)
    parser_plugin = subparsers.add_parser(PLUGIN_NAME, help='plugin main command')
    parser_plugin.set_defaults(func=plugin)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

