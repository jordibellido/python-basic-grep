#!/usr/bin/python3

"""
Yet another grep implementation :-)
"""

import sys
import argparse

from search import Search

def main (argv):
    """ Main function """

    arg_parser = argparse.ArgumentParser (description = 'Yet another grep implementation')

    arg_parser.add_argument ('-r', '--regex', help = 'the regular expression to search for',
                        dest='regex', required = True, type = str)

    arg_parser.add_argument ('-f', '--files', help = 'a list of ﬁles to search in',
                        default = sys.stdin, nargs = '+', type = argparse.FileType ('r'))

    arg_parser.add_argument ('-d', '--debug', help = 'show additional debug information',
                        default = False, action = 'store_true')

    xor_options = arg_parser.add_mutually_exclusive_group ()

    xor_options.add_argument ('-u', '--underline', help = '^ printed underneath the matched text',
                        default = False, action = 'store_true')

    xor_options.add_argument ('-c', '--colo', help = 'the matched text is highlighted in color',
                        default = False, action = 'store_true')

    xor_options.add_argument ('-m', '--machine', help = 'print the output in the agreed format',
                        default = False, action = 'store_true')

    arguments = arg_parser.parse_args (args = argv)

    if arguments.debug is True:
        print (arguments)

    new_search = Search      (arguments.regex, arguments.files, arguments.underline, arguments.colo, arguments.machine)
    new_search.re_search     ()
    new_search.print_results ()

if __name__ == "__main__":
    main (sys.argv[1:])
