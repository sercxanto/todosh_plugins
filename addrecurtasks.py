#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""
    addrecurtasks.py

    Add recurring tasks from recur.txt for the next 10 days (plugin for todo.sh)
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
PLUGIN_NAME = "addrecurtasks"

def usage(args):
    '''Usage message for todo.sh plugin system'''
    print("    " + PLUGIN_NAME + ": " +
            "Adds tasks from recur.txt to todo.txt for next 10 days")
    print("      Non-scheduled tasks will be added as is.")


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

    recur_filename = os.path.join(todo_dir, "recur.txt")

    if not os.path.isfile(recur_filename):
        print("recur.txt not found in TODO_DIR! Exit.", file=sys.stderr)
        sys.exit(1)

    now = datetime.date.today()
    agenda_data = libtodotxt.readtodotxt(recur_filename)

    line_nrs = libtodotxt.get_threshold_line_nr(agenda_data, now, 10)


    print(line_nrs)



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

