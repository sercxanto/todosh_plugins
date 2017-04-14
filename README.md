This repository contains some plugins for Gina's [todo.txt
CLI](https://github.com/ginatrapani/todo.txt-cli). Other noteable plugins are
[schedule](https://github.com/FND/todo.txt-cli/blob/extensions/schedule) and
the [futureTasks
filter](https://github.com/FND/todo.txt-cli/blob/extensions/futureTasks).


addfuturetasks
==============

Add tasks for the next 10 days from the file future.txt to todo.txt. The idea
is to collect tasks with threshold dates for the far future in a seperate file
to not overload todo.txt .


addrecurtasks
=============

Adds recuring tasks from recur.txt to todo.txt. The idea is to regularly call
the script which then adds tasks within the next 10 days to todo.txt. This way
todo.txt stays small and can be used with software not supporting the recur
format.

The format for recur.txt is roughly the same as described in
[topydo](https://github.com/bram85/topydo/wiki/Recurrence) and
[simpletask](https://github.com/mpcjanssen/simpletask-android/blob/master/src/main/assets/index.en.md#extensions):

    Task t:2015-01-01 rec:1y

Implementation details:

* Only threshold/start date ("t:") is considered
* When adding to todo.txt the rec key "rec:" is ommited to not confuse
  software supporting it.
* The current threshold date is the one in todo.txt.
* The next threshold date is the one in recur.txt . When adding
  the task to todo.txt it is incremented.
* The following intervals are supported:
    * "y": Year
    * "m": month
    * "w": week
    * "d": day


agenda
======

Prints an agenda overview of scheduled tasks for the next days. The tasks are
sorted according to date with the line number prefixed. Sample output:

    $ t agenda
    Sun, 2016-08-28:
      24 Work 30min on +stuff t:2016-08-28
      06 2016-08-28 Domain-Registration example.com +admin t: t:2016-08-28

    Mon, 2016-08-29:
      09 @waiting Feedback Jon +project t:2016-08-29
      27 Weekly Backup +admin t:2016-08-29
      19 Ask for doctor appointment t:2016-08-29

    Tue, 2016-08-30:
      25 Do more stuff on +projectx t:2016-08-30

