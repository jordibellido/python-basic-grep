"""
Search class
"""

import re
import sys
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

        # Where the pair (start_pos, end_pos) will be stored for matches
        self.results     = []

        # Where the text lines will be stored for matches
        self.lines       = []

        # Where the text line numbers will be stored for matches
        self.line_no     = []

        # Where the file index from self.files will be stored for matches
        self.files_index = []

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
            elif isinstance (self.files, str) and len (self.files) <= 0:
                raise ValueError ('The parameter files is empty')
            elif 'pytest' in sys.argv[0]:
                # Try to determine if the input has been redirected by pytest to NULL.
                # ELSE case: we will assume that the files parameter is an
                #            object with type _pytest.capture.DontReadFromInput.
                if (
                       isinstance (self.files, bool)
                    or isinstance (self.files, int)
                    or isinstance (self.files, float)
                    or isinstance (self.files, complex)
                    or isinstance (self.files, list)
                    or isinstance (self.files, tuple)
                    or isinstance (self.files, range)
                    or isinstance (self.files, dict)
                    or isinstance (self.files, set)
                    or isinstance (self.files, frozenset)
                    or isinstance (self.files, bytes)
                    or isinstance (self.files, bytearray)
                    or isinstance (self.files,  memoryview)
                ):
                    raise ValueError (
                        f"Invalid type for the parameter files: expected <list> or <string> or stdin, got {type (self.files)}"
                    )
            elif not hasattr (self.files, 'name') or self.files.name != '<stdin>':
                raise ValueError ('The parameter files is not stdin, nor a string nor a list')

        if isinstance (self.files, list):
            if len (self.files) <= 0:
                raise ValueError ('The parameter files is empty')

            # Testing the list of files
            for file in self.files:
                if isinstance (file, str) and len (file) <= 0:
                    raise ValueError ('A file from the parameter files is empty')

                if not isfile (file.name):
                    raise IOError (f"File '{file.name}' does not exist")

                if not access (file.name, R_OK):
                    raise IOError (f"File '{file.name}' is not readable")

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



    def re_search (self):
        """
        Search for the regular expression in the given stream.

        :return: nothing
        """
        current_line_number        = 0
        current_match_index        = 0
        current_file_index         = 0
        previous_line_number_match = -1

        for element in self.files:
            for line in open (file = element.name, mode = 'r', encoding = 'ASCII'):
                for match in re.finditer (self.regex, line, re.ASCII):
                    if previous_line_number_match == current_line_number:
                        # There is at least an additional match within the same line
                        current_match_index -= 1
                        self.results[current_match_index].append ([match.start (), match.end ()])
                    else:
                        self.files_index.append (current_file_index)
                        self.line_no.append     (current_line_number)
                        self.lines.append       (line)
                        self.results.append     ([[match.start (), match.end ()]])
                        current_match_index += 1
                        previous_line_number_match = current_line_number

                current_line_number += 1

            current_line_number = 1
            current_file_index += 1

    def print_results (self):
        """
        Print the results from the last regex search according to the given parameters.
        The script's output format should be: file_name line_number line

        :return: nothing
        """
        current_line_number_index = 0

        if len (self.results) <= 0:
            return

        for result in self.results:
            if len (result) == 1:
                current_line_number_index += 1

            print (
                f"{self.files[self.files_index[current_line_number_index]].name}",
                f"{self.line_no[current_line_number_index]}",
                f"{self.lines[current_line_number_index].rstrip ()}"
            )
