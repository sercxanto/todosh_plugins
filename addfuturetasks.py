#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""
    addfuturetasks.py

    Add tasks tasks for the next 10 days from future.txt(plugin for todo.sh)
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
import sys
import libtodotxt

# Name of the plugin (shell wrapper script)
PLUGIN_NAME = "addfuturetasks"

def usage(args):
    '''Usage message for todo.sh plugin system'''
    print("    " + PLUGIN_NAME + ": " +
            "Adds tasks from future.txt to todo.txt for next 10 days")
    print("      Non-scheduled tasks will be added as is.")


def plugin(args):
    '''Plugin main logic'''

    todo_dir = os.environ.get("TODO_DIR")
    if todo_dir == None:
        print("Env variable TODO_DIR not set! Exit.", file=sys.stderr)
        sys.exit(1)

    preserve_line_nrs = os.environ.get("TODOTXT_PRESERVE_LINE_NUMBERS")
    if preserve_line_nrs == "1":
        preserve_line_nrs = True
    else:
        preserve_line_nrs = False

    todo_filename = os.path.join(todo_dir, "todo.txt")
    if not os.path.isfile(todo_filename):
        print("todo.txt not found in TODO_DIR! Exit.", file=sys.stderr)
        sys.exit(1)

    future_filename = os.path.join(todo_dir, "future.txt")

    if not os.path.isfile(future_filename):
        print("future.txt not found in TODO_DIR! Exit.", file=sys.stderr)
        sys.exit(1)

    now = datetime.date.today()
    agenda_data = libtodotxt.readtodotxt(future_filename)

    lines_to_copy = libtodotxt.get_threshold_line_nr(agenda_data, now, 10)
    if len(lines_to_copy) > 0:
        print("Move the following entries from future.txt to todo.txt:")
        for date in agenda_data:
            for entry in agenda_data[date]:
                if entry["nr"] in lines_to_copy:
                    print("%02d %s" % (entry["nr"], entry["line"]))
        if args.dryrun:
            print("Dry run. Not changing files.")
        else:
            libtodotxt.move_lines(future_filename, todo_filename,
                    lines_to_copy, preserve_line_nrs)
    else:
        print("No future tasks found")


def main():
    '''main function'''
    parser = argparse.ArgumentParser(prog=PLUGIN_NAME)
    subparsers = parser.add_subparsers()
    parser_usage = subparsers.add_parser('usage',
            help='show usage message')
    parser_usage.set_defaults(func=usage)
    parser_plugin = subparsers.add_parser(PLUGIN_NAME,
            help='plugin main command')
    parser_plugin.add_argument("-n", "--dryrun", action="store_true",
            help="Dry run. Do not change files.")
    parser_plugin.set_defaults(func=plugin)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

