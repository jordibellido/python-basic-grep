#!/usr/bin/python3

"""
Yet another grep implementation :-)
"""

import sys
import getopt

def print_help (error_message = ''):
    """ Print the help message for this program """
    if isinstance (error_message, str) and len (error_message) > 0:
        print ("ERROR: ", error_message)

    # This is a simplified help message just for this exercise
    print ('Usage: grep.py -r, --regex myregularexpression [OPTIONAL_OPTIONS]')

def main (argv):
    """ Main function """
    param_debug     = False
    param_underline = False
    param_color     = False
    param_machine   = False
    param_regex     = ''
    param_files     = ''

    if len (sys.argv) <= 1:
        print_help ('Not enough parameters')
        sys.exit   (1)

    try:
        opts, _ = getopt.getopt (
            argv,
            "hucmr:f:",
            ["help", "underline", "colo", "color", "machine", "regex=","files="]
        )
    except getopt.GetoptError:
        print_help ()
        sys.exit   (2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help ()
            sys.exit   (0)
        elif opt in ("-u", "--underline"):
            param_underline = True
        elif opt in ("-c", "--colo", "--color"):
            if not param_underline:
                param_color     = True
        elif opt in ("-m", "--machine"):
            if not param_underline and not param_color:
                param_machine   = True
        elif opt in ("-r", "--regex"):
            param_regex = arg
        elif opt in ("-f", "--files"):
            param_files = arg

    if not isinstance (param_regex, str) or len (param_regex) <= 0:
        print_help ()
        sys.exit   (3)

    if param_debug:
        print ("Parameter underline is set to ", bool (param_underline))
        print ("Parameter color is set to     ", bool (param_color))
        print ("Parameter machine is set to   ", param_machine)
        print ("Parameter regex is set to     ", param_regex)
        print ("Parameter files is set to     ", param_files)

if __name__ == "__main__":
    main (sys.argv[1:])
