"""
Search class
"""

import re
import sys
from   io import TextIOWrapper
from   os import access, R_OK
from   os.path import isfile

class Search:
    """ Search class """

    def __init__ (self, regex, files, underline, color, machine):
        """
        Create a new Search instance

        :param regex: string - the regular expression to search for.
        :param files: list - a list of files to search in.
        :param underline: boolean - ^ printed underneath the matched text.
        :param color: boolean - the matched text is highlighted in color.
        :param machine: boolean - print the output in the agreed format.
        """
        self.regex     = regex
        self.files     = files
        self.underline = underline
        self.color     = color
        self.machine   = machine

        if not isinstance (regex, str):
            raise ValueError ('The parameter regex is not a string variable')

        if len (self.regex) <= 0:
            raise ValueError ('The parameter regex is empty')

        try:
            re.compile (self.regex)
        except re.error:
            raise RuntimeError from re.error (f'The regexp pattern {self.regex} is not valid')

        if not isinstance (files, list):
            if self.files is None:
                self.files = sys.stdin
            elif not isinstance (self.files, TextIOWrapper):
                raise ValueError ('The parameter files is not a list')

        if isinstance (self.files, list):
            if len (self.files) <= 0:
                raise ValueError ('The parameter files is empty')

            # Testing the list of files
            for file in self.files:
                if not isfile (file):
                    raise IOError (f"File '{file}' does not exist")

                if not access (file, R_OK):
                    raise IOError (f"File '{file}' is not readable")

        if not isinstance (underline, bool):
            raise ValueError ('The parameter underline is not a boolean variable')

        if not isinstance (color, bool):
            raise ValueError ('The parameter color is not a boolean variable')

        if not isinstance (machine, bool):
            raise ValueError ('The parameter machine is not a boolean variable')



        # Testing mutual exclusion
        if self.underline is True and self.color is True and self.underline is True:
            raise ValueError ('The parameters underline, colo and underline are mutually exclusive')

        if self.underline is True and self.color is True:
            raise ValueError ('The parameters underline and colo are mutually exclusive')

        if self.color is True and self.machine is True:
            raise ValueError ('The parameters colo and machine are mutually exclusive')

        if self.machine is True and self.underline is True:
            raise ValueError ('The parameters machine and underline are mutually exclusive')



    def search (self):
        """ XXX """
        pass

    def print_results (self, results_list):
        """ XXX """
        pass
