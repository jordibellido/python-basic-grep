"""
Unit testing for the search.py module
"""

from   io import TextIOWrapper
import tempfile
import pytest
from   search import Search

##### Tests for the Search class
def test_regex_is_empty ():
    """ Test MAIN-001: regex is empty """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search ('', [], False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_regex_is_not_valid ():
    """ Test MAIN-002: regex is not valid """
    with pytest.raises (RuntimeError) as pytest_wrapped_e:
        Search ('[*', [], False, False, False)
        assert pytest_wrapped_e.type == RuntimeError

def test_regex_is_not_an_string_1 ():
    """ Test MAIN-003: regex is not an string 1 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search ({}, [], False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_regex_is_not_an_string_2 ():
    """ Test MAIN-004: regex is not an string 2 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search (3.1415926535, [], False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_regex_is_valid_1 ():
    """ Test MAIN-005: regex is valid 1 """
    f005 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    Search ("The quick brown fox*", [f005.name], False, False, False)

def test_regex_is_valid_2 ():
    """ Test MAIN-006: regex is valid 2 """
    f006 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    Search (r'\d+', [f006.name], False, False, False)



def test_files_is_empty ():
    """ Test MAIN-007: files is empty """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search (r'\d+', [], False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_files_is_not_a_list_1 ():
    """ Test MAIN-008: files is not a list 1 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search (r'\d+', '', False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_files_is_not_a_list_2 ():
    """ Test MAIN-009: files is not a list 2 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search (r'\d+', 1.6180339887, False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_files_is_valid_1 ():
    """ Test MAIN-010: files is valid 1 """
    f010 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s010 = Search ("The quick brown fox*", [f010.name], False, False, False)
    assert isinstance (s010.files, list)

def test_files_is_valid_2 ():
    """ Test MAIN-011: files is valid 2 """
    f011 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s011 = Search (r'\d+', [f011.name], False, False, False)
    assert isinstance (s011.files, list)



def test_underline_is_not_a_bool_1 ():
    """ Test MAIN-012: files is not a bool 1 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f012 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f012.name], 0x007, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_underline_is_not_a_bool_2 ():
    """ Test MAIN-013: files is not a bool 2 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f013 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f013.name], [], False, False)
        assert pytest_wrapped_e.type == ValueError

def test_underline_is_not_a_bool_3 ():
    """ Test MAIN-014: files is not a bool 3 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f014 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f014.name], 'trustmeimanengineer', False, False)
        assert pytest_wrapped_e.type == ValueError

def test_underline_is_valid_1 ():
    """ Test MAIN-015: files is valid 1 """
    f015 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s015 = Search ("The quick brown fox*", [f015.name], True, False, False)
    assert s015.underline is True

def test_underline_is_valid_2 ():
    """ Test MAIN-016: files is valid 2 """
    f016 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s016 = Search (r'\d+', [f016.name], False, False, False)
    assert s016.underline is False



def test_color_is_not_a_bool_1 ():
    """ Test MAIN-017: color is not a bool 1 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f017 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f017.name], False, 0x007, False)
        assert pytest_wrapped_e.type == ValueError

def test_color_is_not_a_bool_2 ():
    """ Test MAIN-018: color is not a bool 2 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f018 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f018.name], False, [], False)
        assert pytest_wrapped_e.type == ValueError

def test_color_is_not_a_bool_3 ():
    """ Test MAIN-019: color is not a bool 3 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f019 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f019.name], True, 'trustmeimanengineer', False)
        assert pytest_wrapped_e.type == ValueError

def test_color_is_valid_1 ():
    """ Test MAIN-020: color is valid 1 """
    f020 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s020 = Search ("The quick brown fox*", [f020.name], False, True, False)
    assert s020.color is True

def test_color_is_valid_2 ():
    """ Test MAIN-021: color is valid 2 """
    f021 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s021 = Search (r'\d+', [f021.name], False, False, False)
    assert s021.color is False



def test_machine_is_not_a_bool_1 ():
    """ Test MAIN-022: machine is not a bool 1 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f022 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f022.name], False, False, 0x007)
        assert pytest_wrapped_e.type == ValueError

def test_machine_is_not_a_bool_2 ():
    """ Test MAIN-023: machine is not a bool 2 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f023 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f023.name], False, False, [])
        assert pytest_wrapped_e.type == ValueError

def test_machine_is_not_a_bool_3 ():
    """ Test MAIN-024: machine is not a bool 3 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f024 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f024.name], True, False, 'trustmeimanengineer')
        assert pytest_wrapped_e.type == ValueError

def test_machine_is_valid_1 ():
    """ Test MAIN-025: machine is valid 1 """
    f025 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s025 = Search ("The quick brown fox*", [f025.name], False, False, True)
    assert s025.machine is True

def test_machine_is_valid_2 ():
    """ Test MAIN-026: machine is valid 2 """
    f026 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s026 = Search (r'\d+', [f026.name], False, False, False)
    assert s026.machine is False



def test_mutual_exlusion_1 ():
    """ Test MAIN-027: mutual exclusion 1 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f027 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f027.name], True, True, True)
        assert pytest_wrapped_e.type == ValueError

def test_mutual_exlusion_2 ():
    """ Test MAIN-028: mutual exclusion 2 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f028 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f028.name], True, True, False)
        assert pytest_wrapped_e.type == ValueError

def test_mutual_exlusion_3 ():
    """ Test MAIN-029: mutual exclusion 3 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f029 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f029.name], True, False, True)
        assert pytest_wrapped_e.type == ValueError

def test_mutual_exlusion_4 ():
    """ Test MAIN-030: mutual exclusion 4 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f030 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f030.name], False, True, True)
        assert pytest_wrapped_e.type == ValueError

def test_mutual_exlusion_5 ():
    """ Test MAIN-031: mutual exclusion 5 """
    f031 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s031 = Search (r'\d+', [f031.name], False, False, False)
    assert s031.underline is False
    assert s031.color is False
    assert s031.machine is False

def test_mutual_exlusion_6 ():
    """ Test MAIN-032: mutual exclusion 6 """
    f032 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s032 = Search (r'\d+', [f032.name], True, False, False)
    assert s032.underline is True
    assert s032.color is False
    assert s032.machine is False

def test_mutual_exlusion_7 ():
    """ Test MAIN-033: mutual exclusion 7 """
    f033 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s033 = Search (r'\d+', [f033.name], False, True, False)
    assert s033.underline is False
    assert s033.color is True
    assert s033.machine is False

def test_mutual_exlusion_8 ():
    """ Test MAIN-034: mutual exclusion 8 """
    f034 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s034 = Search (r'\d+', [f034.name], False, False, True)
    assert s034.underline is False
    assert s034.color is False
    assert s034.machine is True



def test_files_do_not_exist_1 ():
    """ Test MAIN-035: a single file does not exist """
    f035 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search (r'\d+', f035.name, False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_files_do_not_exist_2 ():
    """ Test MAIN-036: two files do not exist """
    with pytest.raises (OSError) as pytest_wrapped_e:
        Search (r'\d+', ['', ''], False, False, False)
        assert pytest_wrapped_e.type == OSError

def test_files_do_not_exist_3 ():
    """ Test MAIN-037: three files do not exist """
    with pytest.raises (OSError) as pytest_wrapped_e:
        Search (r'\d+', ['', 'LoremIpsum', ''], False, False, False)
        assert pytest_wrapped_e.type == OSError

def test_files_do_exist_1 ():
    """ Test MAIN-038: one file that does exist """
    f038 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s038 = Search (r'\d+', [f038.name], False, False, False)
    assert s038.files[0] == f038.name

def test_files_do_exist_2 ():
    """ Test MAIN-039: two files that do exist """
    f039a = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    f039b = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s039 = Search (r'\d+', [f039a.name, f039b.name], False, False, False)
    assert s039.files[0] == f039a.name
    assert s039.files[1] == f039b.name

def test_files_do_exist_3 ():
    """ Test MAIN-040: three files that do exist """
    f040a = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    f040b = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    f040c = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s040 = Search (r'\d+', [f040a.name, f040b.name, f040c.name], False, False, False)
    assert s040.files[0] == f040a.name
    assert s040.files[1] == f040b.name
    assert s040.files[2] == f040c.name

def test_files_some_do_exist ():
    """ Test MAIN-041: two files that do exist and one that does not exist """
    f041a = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    f041c = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')

    with pytest.raises (OSError) as pytest_wrapped_e:
        s041 = Search (r'\d+', [f041a.name, '', f041c.name], False, False, False)
        assert s041.files[0] == f041a.name
        assert s041.files[1] == ''
        assert s041.files[2] == f041c.name
        assert pytest_wrapped_e.type == OSError

def test_files_no_permissions ():
    """ Test MAIN-042: a single file with not the right permissions """
    with pytest.raises (OSError) as pytest_wrapped_e:
        Search (r'\d+', ['/etc/sudoers'], False, False, False)
        assert pytest_wrapped_e.type == OSError

def test_files_is_stdin ():
    """ Test MAIN-043: files is not set; that is, STDIN has to be used """
    s043 = Search (r'\d+', None, False, False, False)
    assert isinstance (s043.files, TextIOWrapper)
