"""
Unit testing for the grep.py program
"""

from   os import linesep
import pytest
from   grep import main

HELP_TEXT_LINE_1 = 'usage: __main__.py [-h] -r REGEX [-f [FILES]] [-d] [-u | -c | -m]'
HELP_TEXT_LINE_2 = '__main__.py: error: the following arguments are required: -r/--regex'
HELP_TEXT_LINE_3 = '__main__.py: error: unrecognized arguments: -w'

##### Tests for the function 'main'
def test_string_is_empty (capsys):
    """ Test MAIN-001: string is empty """

    with pytest.raises (SystemExit) as pytest_wrapped_e:
        main ('')
        captured = capsys.readouterr ()

        lines = captured.out.split (linesep)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
        assert lines[0] == HELP_TEXT_LINE_1
        assert lines[1] == HELP_TEXT_LINE_2

def test_main_with_no_arguments (capsys):
    """ Test MAIN-002: arguments list is empty """
    with pytest.raises (SystemExit) as pytest_wrapped_e:
        main ([])
        captured = capsys.readouterr ()

        lines = captured.out.split (linesep)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
        assert lines[0] == HELP_TEXT_LINE_1
        assert lines[1] == HELP_TEXT_LINE_2

def test_main_with_a_madeup_argument_1 (capsys):
    """ Test MAIN-003: only a single made-up argument is passed """
    with pytest.raises (SystemExit) as pytest_wrapped_e:
        main (['-w'])
        captured = capsys.readouterr ()

        lines = captured.out.split (linesep)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
        assert lines[0] == HELP_TEXT_LINE_1
        assert lines[1] == HELP_TEXT_LINE_2

def test_main_with_a_madeup_argument_2 (capsys):
    """ Test MAIN-004: a valid argument and a made-up argument are passed """
    with pytest.raises (SystemExit) as pytest_wrapped_e:
        main (['-r "*"', '-w'])
        captured = capsys.readouterr ()

        lines = captured.out.split (linesep)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
        assert lines[0] == HELP_TEXT_LINE_1
        assert lines[1] == HELP_TEXT_LINE_3

def test_main_h_parameter (capsys):
    """ Test MAIN-005: only the -h argument is passed """
    with pytest.raises (SystemExit) as pytest_wrapped_e:
        main (['-h'])
        captured = capsys.readouterr ()

        lines = captured.out.split (linesep)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
        assert lines[0] == HELP_TEXT_LINE_1

def test_main_exlusive_parameters_1 (capsys):
    """ Test MAIN-006: testing exclusive options - 1 """
    with pytest.raises (SystemExit) as pytest_wrapped_e:
        main (['-u', '-c', '-m'])
        captured = capsys.readouterr ()

        lines = captured.out.split (linesep)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
        assert lines[0] == HELP_TEXT_LINE_1
        assert lines[1] == '__main__.py: error: argument -c/--colo: not allowed with argument -u/--underline'

def test_main_exlusive_parameters_2 (capsys):
    """ Test MAIN-007: testing exclusive options - 2 """
    with pytest.raises (SystemExit) as pytest_wrapped_e:
        main (['-m', '-c'])
        captured = capsys.readouterr ()

        lines = captured.out.split (linesep)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
        assert lines[0] == HELP_TEXT_LINE_1
        assert lines[1] == '__main__.py: error: argument -c/--colo: not allowed with argument -m/--machine'

def test_main_exlusive_parameters_3 (capsys):
    """ Test MAIN-008: testing exclusive options - 3 """
    with pytest.raises (SystemExit) as pytest_wrapped_e:
        main (['-c', '-m'])
        captured = capsys.readouterr ()

        lines = captured.out.split (linesep)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
        assert lines[0] == HELP_TEXT_LINE_1
        assert lines[1] == '__main__.py: error: argument -m/--machine: not allowed with argument -c/--colo'

def test_main_exlusive_parameters_4 (capsys):
    """ Test MAIN-009: testing exclusive options - 4 """
    with pytest.raises (SystemExit) as pytest_wrapped_e:
        main (['-u', '-m'])
        captured = capsys.readouterr ()

        lines = captured.out.split (linesep)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
        assert lines[0] == HELP_TEXT_LINE_1
        assert lines[1] == '__main__.py: error: argument -m/--machine: not allowed with argument -u/--underline'

def test_main_exlusive_parameters_5 (capsys):
    """ Test MAIN-010: testing exclusive options - 5 """
    with pytest.raises (SystemExit) as pytest_wrapped_e:
        main (['-m', '-u'])
        captured = capsys.readouterr ()

        lines = captured.out.split (linesep)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
        assert lines[0] == HELP_TEXT_LINE_1
        assert lines[1] == '__main__.py: error: argument -u/--underline: not allowed with argument -m/--machine'

def test_main_exlusive_parameters_6 (capsys):
    """ Test MAIN-011: testing exclusive options - 6 """
    with pytest.raises (SystemExit) as pytest_wrapped_e:
        main (['-c', '-m'])
        captured = capsys.readouterr ()

        lines = captured.out.split (linesep)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
        assert lines[0] == HELP_TEXT_LINE_1
        assert lines[1] == '__main__.py: error: argument -m/--machine: not allowed with argument -c/--colo'

def test_main_exlusive_parameters_7 (capsys):
    """ Test MAIN-012: testing exclusive options - 7 """
    with pytest.raises (SystemExit) as pytest_wrapped_e:
        main (['-m', '-c'])
        captured = capsys.readouterr ()

        lines = captured.out.split (linesep)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
        assert lines[0] == HELP_TEXT_LINE_1
        assert lines[1] == '__main__.py: error: argument -c/--colo: not allowed with argument -m/--machine'

def test_main_r_parameter_1 (capsys):
    """ Test MAIN-013: only the -r argument is passed """
    with pytest.raises (SystemExit) as pytest_wrapped_e:
        main (['-r'])
        captured = capsys.readouterr ()

        lines = captured.out.split (linesep)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
        assert lines[0] == HELP_TEXT_LINE_1
        assert lines[1] == '__main__.py: error: argument -r/--regex: expected one argument'

def test_main_r_parameter_2 (capsys):
    """ Test MAIN-014: only the --regex argument is passed """
    with pytest.raises (SystemExit) as pytest_wrapped_e:
        main (['--regex'])
        captured = capsys.readouterr ()

        lines = captured.out.split (linesep)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
        assert lines[0] == HELP_TEXT_LINE_1
        assert lines[1] == '__main__.py: error: argument -r/--regex: expected one argument'

def test_main_r_parameter_3 (capsys):
    """ Test MAIN-015: only a valid -r argument is passed """
    main (['-r "aaa"'])
    captured = capsys.readouterr ()

    lines = captured.out.split (linesep)
    assert lines[0] == ''

def test_main_r_parameter_4 (capsys):
    """ Test MAIN-016: only a valid --regex argument is passed """
    main (['--regex', 'README.md'])
    captured = capsys.readouterr ()

    lines = captured.out.split (linesep)
    assert lines[0] == ''

def test_main_f_parameter_1 (capsys):
    """ Test MAIN-017: only the -f argument is passed """
    with pytest.raises (SystemExit) as pytest_wrapped_e:
        main (['-f'])
        captured = capsys.readouterr ()

        lines = captured.out.split (linesep)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
        assert lines[0] == HELP_TEXT_LINE_1
        assert lines[1] == '__main__.py: error: the following arguments are required: -r/--regex'

def test_main_f_parameter_2 (capsys):
    """ Test MAIN-018: only the --files argument is passed """
    with pytest.raises (SystemExit) as pytest_wrapped_e:
        main (['--files'])
        captured = capsys.readouterr ()

        lines = captured.out.split (linesep)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2
        assert lines[0] == HELP_TEXT_LINE_1
        assert lines[1] == '__main__.py: error: the following arguments are required: -r/--regex'

def test_main_f_parameter_3 (capsys):
    """ Test MAIN-019: arguments -r and --files are passed """
    main (['-r', '*', '--files'])
    captured = capsys.readouterr ()

    lines = captured.out.split (linesep)
    assert lines[0] == ''

def test_main_d_parameter_1 (capsys):
    """ Test MAIN-020: the -r and the -d parameters are passed """
    main (['-r', 'dummyregexp', '-d'])
    captured = capsys.readouterr ()

    lines = captured.out.split (linesep)
    assert lines[0].startswith ("Namespace(colo=False, debug=True, files=")
    assert lines[0].endswith ("machine=False, regex='dummyregexp', underline=False)")

def test_main_d_parameter_2 (capsys):
    """ Test MAIN-021: the --regex and the --debug parameters are passed """
    main (['--regex', 'dummyregexp', '--debug'])
    captured = capsys.readouterr ()

    lines = captured.out.split (linesep)
    assert lines[0].startswith ("Namespace(colo=False, debug=True, files=")
    assert lines[0].endswith ("machine=False, regex='dummyregexp', underline=False)")

def test_main_d_parameter_3 (capsys):
    """ Test MAIN-022: the --regex, the --machine and the --debug parameters are passed """
    main (['--machine', '--regex', 'dummyregexp', '--debug'])
    captured = capsys.readouterr ()

    lines = captured.out.split (linesep)
    assert lines[0].startswith ("Namespace(colo=False, debug=True, files=")
    assert lines[0].endswith ("machine=True, regex='dummyregexp', underline=False)")

def test_main_d_parameter_4 (capsys):
    """ Test MAIN-023: the -r, the --underline and the -d parameters are passed """
    main (['--underline', '-r', 'dummyregexp', '-d'])
    captured = capsys.readouterr ()

    lines = captured.out.split (linesep)
    assert lines[0].startswith ("Namespace(colo=False, debug=True, files=")
    assert lines[0].endswith ("machine=False, regex='dummyregexp', underline=True)")

def test_main_d_parameter_5 (capsys):
    """ Test MAIN-024: the -r, the --colo and the --debug parameters are passed """
    main (['--colo', '-r', 'dummyregexp', '--debug'])
    captured = capsys.readouterr ()

    lines = captured.out.split (linesep)
    assert lines[0].startswith ("Namespace(colo=True, debug=True, files=")
    assert lines[0].endswith ("machine=False, regex='dummyregexp', underline=False)")

def test_main_d_parameter_6 (capsys):
    """ Test MAIN-025: the -r, the -m and the -d parameters are passed """
    main (['-m', '-r', 'dummyregexp', '-d'])
    captured = capsys.readouterr ()

    lines = captured.out.split (linesep)
    assert lines[0].startswith ("Namespace(colo=False, debug=True, files=")
    assert lines[0].endswith ("machine=True, regex='dummyregexp', underline=False)")
