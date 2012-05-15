#! /usr/bin/env python3

#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc.
"""
Common and simple functions that are used throughout everything else.
"""

import multiprocessing
import os
import subprocess
import sys
import tempfile

def error(message):
  sys.stderr.write(message + '\n')

roman_numeral_map = (('m',  1000), ('cm', 900), ('d',  500),
                     ('cd', 400), ('c',  100), ('xc', 90),
                     ('ix', 9), ('v',  5), ('iv', 4), ('i',  1))
html_codes = (['&', '&amp;'],['<', '&lt;'],['>', '&gt;'],['"', '&quot;'])

def arabic_to_roman(number):
    """
    convert arabic integer to roman numeral
    """

    roman = ''
    for numeral, integer in roman_numeral_map:
        while number >= integer:
            roman = roman + numeral
            number = number - integer
    return roman

def color(text, color_name):
    """
    Change the text color by adding ANSI escape sequences.
    """

    # Don't bother on the windows platform.
    if sys.platform.startswith('win'):
        return text

    colors = {}
    colors['pink'] = '\033[95m'
    colors['blue'] = '\033[94m'
    colors['green'] = '\033[92m'
    colors['yellow'] = '\033[93m'
    colors['red'] = '\033[91m'
    end = '\033[0m'

    if color_name in colors.keys():
        text = colors[color_name] + text + end

    return text

def counter(start=0, end=None, incriment=1, roman=False):
    """
    Basic generator that increases the return with each call.  The return is a string.
    """

    current = start
    if roman:
        yield arabic_to_roman(current)
    else:
        yield str(current)

    while True:
        if (end is not None) and (current >= end):
            return
        else:
            current = current + incriment
            if roman:
                yield arabic_to_roman(current)
            else:
                yield str(current)

def replace_html_codes(text):
    """
    Replaces html ampersand codes (e.g. &gt;) with their actual character (e.g. >)
    """

    for code in html_codes:
        text = text.replace(code[1], code[0])

    return text

def split_cmd(start, files, end=''):
    """
    Rumor has it that Windows has a character limit of a little more than 32,000 for commands.[1]
    Linux seems to vary based on kernel settings and whatnot, but tends to be more in the millions.[2]
    Supposing the images are named 'page_0001.tif', we can hit the windows limit very quickly.  For the
    sake of being safe, we will split things up at the 32,000 mark.

    [1] http://stackoverflow.com/questions/2381241/what-is-the-subprocess-popen-max-length-of-the-args-parameter
    [2] http://www.linuxjournal.com/article/6060
    """

    cmds = []
    start = start + ' '
    end = ' ' + end

    buffer = start
    while len(files) > 0:
        if len(buffer) + len(files[0]) + len(end) + 3 < 32000:
            buffer = buffer + ' "' + files.pop(0) + '"'
        else:
            buffer = buffer + end.rstrip()
            cmds.append(buffer)
            buffer = start
    buffer = buffer + end.rstrip()
    cmds.append(buffer)

    return cmds

def separate_cmd(cmd):
    """
    Convert a subprocess command string into a list, intelligently handling arguments
    enclosed in single or double quotes.
    """

    cmd = list(cmd)
    buffer = ''
    out = []
    switch = [False, '']

    for x in range(len(cmd)):
        char = cmd[x]
        if char == ' ' and not switch[0]:
            out.append(buffer)
            buffer = ''
        # Be wary of a single/double quote that is part of a filename and not part of an
        # enclosing pair
        elif (char == '"' or char == "'") and not switch[0]:
            if (char in cmd[x+1:]) and (buffer == ''):
                switch[0] = True
                switch[1] = char
            else:
                buffer = buffer + char
        elif char == switch[1] and switch[0]:
            out.append(buffer)
            buffer = ''
            switch[0] = False
        else:
            buffer = buffer + char
    out.append(buffer)

    # Just in case there were multiple spaces.
    while '' in out:
        out.remove('')

    return out

def simple_exec(cmd):
    """
    Execute a simple command.  Any output disregarded and exit status is
    returned.
    """

    with open(os.devnull, 'w') as void:
        sub = subprocess.Popen(cmd, shell=False, stdout=void, stderr=void)
        return int(sub.wait())

def execute(cmd, capture=False):
    """
    Execute a command line process.  Includes the option of capturing output,
    and checks for successful execution.
    """

    with open(os.devnull, 'w') as void:
        if capture:
            sub = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=void)
        else:
            sub = subprocess.Popen(cmd, shell=True, stdout=void, stderr=void)
    status = sub.wait()

    # Exit if the command fails for any reason.
    if status != 0:
        raise ValueError('err: utils.execute(): command exited with bad status.\ncmd = {0}\nexit status = {1}'.format(cmd, status))

    if capture:
        text = sub.stdout.read()
        return text
    else:
        return None

def list_files(directory='.', contains=None, extension=None):
    """Find all files in a given directory that match criteria."""
    tmp = os.listdir(directory)
    contents = []
    for path in tmp:
        path = os.path.join(directory, path)
        if os.path.isfile(path):
            contents.append(path)
    contents.sort()

    if contains is not None:
        remove = []
        for file in contents:
            if contains not in file:
                remove.append(file)
        for file in remove:
            contents.remove(file)

    if extension is not None:
        remove = []
        for file in contents:
            ext = file.split('.')[-1]
            if extension.lower() != ext.lower():
                remove.append(file)
        for file in remove:
            contents.remove(file)

    return contents

def is_executable(command):
    """
    Checks if a given command is available.  Handy for dependency checks on external commands.
    """

    if get_executable_path(command) is not None:
        return True
    else:
        return False


def get_executable_path(command):
    """
    Checks if a given command is available and returns the path to the executable (if available).
    """

    # Add extension if on the windows platform.
    if sys.platform.startswith('win'):
        pathext = os.environ['PATHEXT']
    else:
        pathext = ''

    for path in os.environ['PATH'].split(os.pathsep):
        if os.path.isdir(path):
            for ext in pathext.split(os.pathsep):
                name = os.path.join(path, command + ext)
                if (os.access(name, os.X_OK)) and (not os.path.isdir(name)):
                    return name

    return None

def parse_config(filename):
    """
    Returns a dictionary of config/value pairs from a simple config file without
    sections or the other complexities of the builtin ConfigParser.
    """

    options = {}

    with open(filename) as handle:
        for line in handle:

            line = line.strip()

            # Remove comments.  Note that in-line comments are not handled and
            # will probaly screw something up.
            if line.startswith('#'):
                line = ''

            # Store option/value pairs.
            if '=' in line:
                option, value = line.split('=', 1)

                option = option.strip()
                value = value.strip()

                options[option] = value

    return options

def cpu_count():
    """
    Returns the number of CPU cores (both virtual an pyhsical) in the system.
    """

    try:
        cpus = multiprocessing.cpu_count()
    except (NotImplementedError):
        cpus = 1

    return cpus
