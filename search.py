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
        self.results   = {}

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
        current_line_no = 0
        current_result  = []

        for element in self.files:
            if isinstance (element, str):
                # The input comes from the standard input stream
                for match in re.finditer (self.regex, element, re.ASCII):
                    current_result.append (
                        {
                            'start_pos': match.start (), 'end_pos': match.end (),
                            'line_no': current_line_no, 'line_text': element.rstrip ()
                        }
                    )

                    current_line_no += 1

                if len (current_result) > 0:
                    self.results = {'stdin': current_result}

            else:
                # The input comes from a file stored in a file system
                for line in open (file = element.name, mode = 'r', encoding = 'ASCII'):
                    for match in re.finditer (self.regex, line, re.ASCII):
                        current_result.append (
                            {
                                'start_pos': match.start (), 'end_pos': match.end (),
                                'line_no': current_line_no, 'line_text': line.rstrip ()
                            }
                        )

                    current_line_no += 1

                if len (current_result) > 0:
                    self.results = {element.name: current_result}


    def print_results (self):
        """
        Print the results from the last regex search according to the given parameters.
        The script's output format should be: file_name line_number line

        :return: nothing
        """
        if len (self.results) > 0:
            for file, result in self.results.items ():
                for match in result:
                    if self.machine is True:
                        # Expected output: file_name:line_number:start_position:matched_text
                        print (f"{file}:{match['line_no']}:{match['start_pos']}:{match['line_text'].rstrip ()}")
                    elif self.color is True:
                        # Expected output: the same as the default one, but the matched text is colorized
                        start_pos       = 0
                        match_start_pos = start_pos + match['start_pos']
                        match_end_pos   = start_pos + match['end_pos']
                        colorized_text  = f"{match['line_text'][0:match_start_pos]}\033[1;31m{match['line_text'][match_start_pos:match_end_pos]}\033[00m{match['line_text'][match_end_pos:]}"
                        print (f"{file} {match['line_no']} {colorized_text.rstrip ()}")
                    else:
                        # Expected output: file_name line_number line
                        print (f"{file} {match['line_no']} {match['line_text'].rstrip ()}")

                        if self.underline is True:
                            start_pos       = len (file) + 1 + len (str (match['line_no'])) + 1
                            match_start_pos = start_pos + match['start_pos']
                            match_end_pos   = start_pos + match['end_pos']
                            highlight_text  = '^' * (match_end_pos - match_start_pos)
                            print ((' ' * match_start_pos) + ('^' * (match_end_pos - match_start_pos)))