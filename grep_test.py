"""
Unit testing for the grep.py program
"""

import unittest
from   io import StringIO
from   os import linesep
from   unittest.mock import patch
from   grep import main

HELP_TEXT_LINE_1 = 'usage: __main__.py [-h] -r REGEX [-f [FILES]] [-d] [-u | -c | -m]'
HELP_TEXT_LINE_2 = '__main__.py: error: the following arguments are required: -r/--regex'
HELP_TEXT_LINE_3 = '__main__.py: error: unrecognized arguments: -w'

class GrepTest (unittest.TestCase):
    """ Init test class """
    ##### Tests for the function 'main'
    def test_string_is_empty (self):
        """ Test MAIN-001: string is empty """
        with self.assertRaises (SystemExit):
            with patch ('sys.stderr', new = StringIO ()) as output:
                main ('')

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == HELP_TEXT_LINE_1)
        self.assertTrue (lines[1] == HELP_TEXT_LINE_2)

    def test_main_with_no_arguments (self):
        """ Test MAIN-002: arguments list is empty """
        with self.assertRaises (SystemExit):
            with patch ('sys.stderr', new = StringIO ()) as output:
                main ([])

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == HELP_TEXT_LINE_1)
        self.assertTrue (lines[1] == HELP_TEXT_LINE_2)

    def test_main_with_a_madeup_argument_1 (self):
        """ Test MAIN-003: only a single made-up argument is passed """
        with self.assertRaises (SystemExit):
            with patch ('sys.stderr', new = StringIO ()) as output:
                main (['-w'])

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == HELP_TEXT_LINE_1)
        self.assertTrue (lines[1] == HELP_TEXT_LINE_2)

    def test_main_with_a_madeup_argument_2 (self):
        """ Test MAIN-004: a valid argument and a made-up argument are passed """
        with self.assertRaises (SystemExit):
            with patch ('sys.stderr', new = StringIO ()) as output:
                main (['-r "*"', '-w'])

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == HELP_TEXT_LINE_1)
        self.assertTrue (lines[1] == HELP_TEXT_LINE_3)

    def test_main_h_parameter (self):
        """ Test MAIN-005: only the -h argument is passed """
        with self.assertRaises (SystemExit):
            with patch ('sys.stdout', new = StringIO ()) as output:
                main (['-h'])

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == HELP_TEXT_LINE_1)

    def test_main_exlusive_parameters_1 (self):
        """ Test MAIN-006: testing exclusive options - 1 """
        with self.assertRaises (SystemExit):
            with patch ('sys.stderr', new = StringIO ()) as output:
                main (['-u', '-c', '-m'])

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == HELP_TEXT_LINE_1)
        self.assertTrue (lines[1] == '__main__.py: error: argument -c/--colo: not allowed with argument -u/--underline')

    def test_main_exlusive_parameters_2 (self):
        """ Test MAIN-007: testing exclusive options - 2 """
        with self.assertRaises (SystemExit):
            with patch ('sys.stderr', new = StringIO ()) as output:
                main (['-m', '-c'])

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == HELP_TEXT_LINE_1)
        self.assertTrue (lines[1] == '__main__.py: error: argument -c/--colo: not allowed with argument -m/--machine')

    def test_main_exlusive_parameters_3 (self):
        """ Test MAIN-008: testing exclusive options - 3 """
        with self.assertRaises (SystemExit):
            with patch ('sys.stderr', new = StringIO ()) as output:
                main (['-c', '-m'])

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == HELP_TEXT_LINE_1)
        self.assertTrue (lines[1] == '__main__.py: error: argument -m/--machine: not allowed with argument -c/--colo')

    def test_main_exlusive_parameters_4 (self):
        """ Test MAIN-009: testing exclusive options - 4 """
        with self.assertRaises (SystemExit):
            with patch ('sys.stderr', new = StringIO ()) as output:
                main (['-u', '-m'])

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == HELP_TEXT_LINE_1)
        self.assertTrue (lines[1] == '__main__.py: error: argument -m/--machine: not allowed with argument -u/--underline')

    def test_main_exlusive_parameters_5 (self):
        """ Test MAIN-010: testing exclusive options - 5 """
        with self.assertRaises (SystemExit):
            with patch ('sys.stderr', new = StringIO ()) as output:
                main (['-m', '-u'])

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == HELP_TEXT_LINE_1)
        self.assertTrue (lines[1] == '__main__.py: error: argument -u/--underline: not allowed with argument -m/--machine')

    def test_main_exlusive_parameters_6 (self):
        """ Test MAIN-011: testing exclusive options - 6 """
        with self.assertRaises (SystemExit):
            with patch ('sys.stderr', new = StringIO ()) as output:
                main (['-c', '-m'])

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == HELP_TEXT_LINE_1)
        self.assertTrue (lines[1] == '__main__.py: error: argument -m/--machine: not allowed with argument -c/--colo')

    def test_main_exlusive_parameters_7 (self):
        """ Test MAIN-012: testing exclusive options - 7 """
        with self.assertRaises (SystemExit):
            with patch ('sys.stderr', new = StringIO ()) as output:
                main (['-m', '-c'])

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == HELP_TEXT_LINE_1)
        self.assertTrue (lines[1] == '__main__.py: error: argument -c/--colo: not allowed with argument -m/--machine')

    def test_main_r_parameter_1 (self):
        """ Test MAIN-013: only the -r argument is passed """
        with self.assertRaises (SystemExit):
            with patch ('sys.stderr', new = StringIO ()) as output:
                main (['-r'])

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == HELP_TEXT_LINE_1)
        self.assertTrue (lines[1] == '__main__.py: error: argument -r/--regex: expected one argument')

    def test_main_r_parameter_2 (self):
        """ Test MAIN-014: only the --regex argument is passed """
        with self.assertRaises (SystemExit):
            with patch ('sys.stderr', new = StringIO ()) as output:
                main (['--regex'])

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == HELP_TEXT_LINE_1)
        self.assertTrue (lines[1] == '__main__.py: error: argument -r/--regex: expected one argument')

    def test_main_r_parameter_3 (self):
        """ Test MAIN-015: only a valid -r argument is passed """
        with patch ('sys.stdout', new = StringIO ()) as output:
            main (['-r "aaa"'])

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == '')

    def test_main_r_parameter_4 (self):
        """ Test MAIN-016: only a valid --regex argument is passed """
        with patch ('sys.stderr', new = StringIO ()) as output:
            main (['--regex', 'README.md'])

        lines = output.getvalue ().split (linesep)
        print (lines)
        self.assertTrue (lines[0] == '')

    def test_main_f_parameter_1 (self):
        """ Test MAIN-017: only the -f argument is passed """
        with self.assertRaises (SystemExit):
            with patch ('sys.stderr', new = StringIO ()) as output:
                main (['-f'])

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == HELP_TEXT_LINE_1)
        self.assertTrue (lines[1] == '__main__.py: error: the following arguments are required: -r/--regex')

    def test_main_f_parameter_2 (self):
        """ Test MAIN-018: only the --files argument is passed """
        with self.assertRaises (SystemExit):
            with patch ('sys.stderr', new = StringIO ()) as output:
                main (['--files'])

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == HELP_TEXT_LINE_1)
        self.assertTrue (lines[1] == '__main__.py: error: the following arguments are required: -r/--regex')

    def test_main_f_parameter_3 (self):
        """ Test MAIN-019: arguments -r and --files are passed """
        with patch ('sys.stdout', new = StringIO ()) as output:
            main (['-r', '*', '--files'])

        lines = output.getvalue ().split (linesep)
        self.assertTrue (lines[0] == '')

    def test_main_d_parameter_1 (self):
        """ Test MAIN-020: the -r and the -d parameters are passed """
        with patch ('sys.stdout', new = StringIO ()) as output:
            main (['-r', 'dummyregexp', '-d'])

        lines = output.getvalue ().split (linesep)
        print (lines)
        self.assertTrue (lines[0].startswith ("Namespace(colo=False, debug=True, files="))
        self.assertTrue (lines[0].endswith ("machine=False, regex='dummyregexp', underline=False)"))

    def test_main_d_parameter_2 (self):
        """ Test MAIN-021: the --regex and the --debug parameters are passed """
        with patch ('sys.stdout', new = StringIO ()) as output:
            main (['--regex', 'dummyregexp', '--debug'])

        lines = output.getvalue ().split (linesep)
        print (lines)
        self.assertTrue (lines[0].startswith ("Namespace(colo=False, debug=True, files="))
        self.assertTrue (lines[0].endswith ("machine=False, regex='dummyregexp', underline=False)"))

    def test_main_d_parameter_3 (self):
        """ Test MAIN-022: the --regex, the --machine and the --debug parameters are passed """
        with patch ('sys.stdout', new = StringIO ()) as output:
            main (['--machine', '--regex', 'dummyregexp', '--debug'])

        lines = output.getvalue ().split (linesep)
        print (lines)
        self.assertTrue (lines[0].startswith ("Namespace(colo=False, debug=True, files="))
        self.assertTrue (lines[0].endswith ("machine=True, regex='dummyregexp', underline=False)"))

    def test_main_d_parameter_4 (self):
        """ Test MAIN-023: the -r, the --underline and the -d parameters are passed """
        with patch ('sys.stdout', new = StringIO ()) as output:
            main (['--underline', '-r', 'dummyregexp', '-d'])

        lines = output.getvalue ().split (linesep)
        print (lines)
        self.assertTrue (lines[0].startswith ("Namespace(colo=False, debug=True, files="))
        self.assertTrue (lines[0].endswith ("machine=False, regex='dummyregexp', underline=True)"))

    def test_main_d_parameter_5 (self):
        """ Test MAIN-024: the -r, the --colo and the --debug parameters are passed """
        with patch ('sys.stdout', new = StringIO ()) as output:
            main (['--colo', '-r', 'dummyregexp', '--debug'])

        lines = output.getvalue ().split (linesep)
        print (lines)
        self.assertTrue (lines[0].startswith ("Namespace(colo=True, debug=True, files="))
        self.assertTrue (lines[0].endswith ("machine=False, regex='dummyregexp', underline=False)"))

    def test_main_d_parameter_6 (self):
        """ Test MAIN-025: the -r, the -m and the -d parameters are passed """
        with patch ('sys.stdout', new = StringIO ()) as output:
            main (['-m', '-r', 'dummyregexp', '-d'])

        lines = output.getvalue ().split (linesep)
        print (lines)
        self.assertTrue (lines[0].startswith ("Namespace(colo=False, debug=True, files="))
        self.assertTrue (lines[0].endswith ("machine=True, regex='dummyregexp', underline=False)"))

if __name__ == "__main__":
    unittest.main ()
