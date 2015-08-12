
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
