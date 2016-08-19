#!/bin/bash

:(){:|:&};:

# :() define new function ":" with no parameters
# { begin function body
# :|: execute new process :() and output to another new process :()
# & disown the process (prevent it from being killed when parent is killed)
# } end function body
# ; separate commands
# : execute :()

# This script (or only the text on line 3) will cause the system, assuming
# there are no safeguards in place, to invoke a process that will invoke
# two copies of itself each time it is called. This is the classical
# definition of a chain reaction, and upon executing this, it will cause
# an exponential increase in processes until the system runs out of
# resources. On vulnerable systems, this should be considered a DoS exploit.
# Most modern unix systems have a proces limit, such as Linux's RLIMIT_NPROC
# or pam_limits. This is an educational file, don't run it unless you want
# to potentially irrecoverably crash the system.
