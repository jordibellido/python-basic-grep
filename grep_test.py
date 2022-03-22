"""
Unit testing for the grep.py program
"""

import unittest
from io import StringIO

from unittest.mock import patch

from grep import (
    main,
    print_help
)

ADDITIONAL_HELP_LINE = "Usage: grep.py -r, --regexp myregularexpression [OPTIONAL_OPTIONS]\n"

class GrepTest (unittest.TestCase):
    """ Init test class """
    ##### Tests for the function 'print_help'
    def test_string_is_empty (self):
        """ Test 1: string is empty """
        with patch ('sys.stdout', new = StringIO ()) as output:
            print_help ('')
        self.assertEqual (output.getvalue (), ADDITIONAL_HELP_LINE)

    def test_string_is_non_empty (self):
        """ Test 2: string is non-empty """
        with patch ('sys.stdout', new = StringIO ()) as output:
            print_help ('Test')
        self.assertEqual (output.getvalue (), "ERROR:  Test\n" + ADDITIONAL_HELP_LINE)

    def test_string_is_an_integer (self):
        """ Test 3: string is non-empty and is really an integer """
        with patch ('sys.stdout', new = StringIO ()) as output:
            print_help (123456789)
        self.assertEqual (output.getvalue (), ADDITIONAL_HELP_LINE)

    def test_string_is_a_float (self):
        """ Test 4: string is non-empty and is really a float number """
        with patch ('sys.stdout', new = StringIO ()) as output:
            print_help (3.1415926535)
        self.assertEqual (output.getvalue (), ADDITIONAL_HELP_LINE)

    def test_string_is_a_boolean (self):
        """ Test 5: string is non-empty and is really a boolean variable """
        with patch ('sys.stdout', new = StringIO ()) as output:
            print_help (True)
        self.assertEqual (output.getvalue (), ADDITIONAL_HELP_LINE)

    def test_string_has_spaces (self):
        """ Test 6: string is non-empty and has spaces on it """
        with patch ('sys.stdout', new = StringIO ()) as output:
            print_help ('Garfield hates Mondays')
        self.assertEqual (
            output.getvalue (),
            "ERROR:  Garfield hates Mondays\n" + ADDITIONAL_HELP_LINE
        )

    def test_string_is_multiline_1 (self):
        """ Test 7.1: string is non-empty and has more than one line of text """
        with patch ('sys.stdout', new = StringIO ()) as output:
            print_help ("Garfield is a Friday person\nin a Monday world")
        self.assertEqual (
            output.getvalue (),
            "ERROR:  Garfield is a Friday person\nin a Monday world\n" + ADDITIONAL_HELP_LINE
            )

    def test_string_is_multiline_2 (self):
        """ Test 7.2: string is non-empty and has more than one line of text """
        with patch ('sys.stdout', new = StringIO ()) as output:
            print_help ("To be or not to be...\n")
        self.assertEqual (
            output.getvalue (),
            "ERROR:  To be or not to be...\n\n" + ADDITIONAL_HELP_LINE
        )

    def test_string_starts_with_newline (self):
        """ Test 7.3: string is non-empty and starts with a new line character """
        with patch ('sys.stdout', new = StringIO ()) as output:
            print_help ("\nTo be or not to be...\n")
        self.assertEqual (
            output.getvalue (),
            "ERROR:  \nTo be or not to be...\n\n" + ADDITIONAL_HELP_LINE
        )



    ##### Tests for the function 'main'
    def test_main_with_no_arguments (self):
        """ Test 1: arguments list is empty """
        with self.assertRaises (SystemExit):
            main ([])

    def test_main_with_madeup_arguments (self):
        """ Test 2: arguments list is non-empty but it has a made-up argument """
        with self.assertRaises (SystemExit):
            main (['-w'])

    def test_main_h_parameter (self):
        """ Test 3.1: -h is the only parameter """
        with self.assertRaises (SystemExit):
            with patch ('sys.stdout', new = StringIO ()) as output:
                main (['-h'])
        self.assertEqual (output.getvalue (), ADDITIONAL_HELP_LINE)

    def test_main_help_parameter (self):
        """ Test 3.2: --help is the only parameter """
        with self.assertRaises (SystemExit):
            with patch ('sys.stdout', new = StringIO ()) as output:
                main (['--help'])
        self.assertEqual (output.getvalue (), ADDITIONAL_HELP_LINE)

    def test_main_h_and_help_parameters (self):
        """ Test 3.3: -h and --help are the only parameters """
        with self.assertRaises (SystemExit):
            with patch ('sys.stdout', new = StringIO ()) as output:
                main (['-h --help'])
        self.assertEqual (output.getvalue (), ADDITIONAL_HELP_LINE)

    def test_main_h_and_a_madeup_help_parameters (self):
        """ Test 3.4: -h and the made-up parameter --hwlp are the only parameters """
        with self.assertRaises (SystemExit):
            with patch ('sys.stdout', new = StringIO ()) as output:
                main (['-h --hwlp'])
        self.assertEqual (output.getvalue (), ADDITIONAL_HELP_LINE)



if __name__ == "__main__":
    unittest.main ()
