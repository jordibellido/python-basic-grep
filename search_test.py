"""
Unit testing for the search.py module
"""

import os
import tempfile
import pytest
from   search import Search

##### SAMPLE FILE 01
##### Generate a big file (~100 MB) for the search tests.
##### This execution adds 0'35 seconds to this test execution!!!
sample_100MB_file_with_text = tempfile.NamedTemporaryFile (mode = 'w', prefix = 'search_test-')
sample_100MB_file_results   = tempfile.NamedTemporaryFile (mode = 'w', prefix = 'search_test-')

# Generate a 100 MB file from the initial text seed. The sample file is exactly 1024 bytes.
with open (f'{sample_100MB_file_with_text.name}', 'w', encoding = 'ASCII') as fout:
    text_file = open ('data/sample01.txt', 'r', encoding = 'ASCII')
    fout.write (text_file.read () * (100 * 1024))
    text_file.close ()

# Generate the search result for a known regexp for the sample file:
with open (f'{sample_100MB_file_results.name}', 'w', encoding = 'ASCII') as fout:
    text_file = open ('data/result01.txt', 'r', encoding = 'ASCII')
    fout.write ('[')
    fout.write (text_file.read () * ((100 * 1024) - 1))
    fout.write ("['Lorem']")
    fout.write (']')
    text_file.close ()


##### SAMPLE FILE 02
SAMPLE_SQL_FILE_WITH_TEXT = 'data/sample02.sql'
SAMPLE_SQL_FILE_RESULTS   = 'data/result02.txt'



def test_generated_files ():
    """ Test MAIN-000: test generated files sizes """
    # SAMPLE FILES 01
    assert os.path.getsize (sample_100MB_file_with_text.name) == (100 * 1024 * 1024)

    # There are (100 * 1024) occurences of the Lorem word, which is 11-char long,
    # plus the starting and closing bracket, minus the last comma and space
    # (which are not necessary): (100 * 11 * 1024) + 2 - 1 - 1
    assert os.path.getsize (sample_100MB_file_results.name)   == (100 * 11 * 1024)

    # SAMPLE FILES 02
    assert os.path.getsize (SAMPLE_SQL_FILE_WITH_TEXT) == 86561
    assert os.path.getsize (SAMPLE_SQL_FILE_RESULTS)   == 1279



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
    Search ("The quick brown fox*", [f005], False, False, False)

def test_regex_is_valid_2 ():
    """ Test MAIN-006: regex is valid 2 """
    f006 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    Search (r'\d+', [f006], False, False, False)



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
    s010 = Search ("The quick brown fox*", [f010], False, False, False)
    assert isinstance (s010.files, list)

def test_files_is_valid_2 ():
    """ Test MAIN-011: files is valid 2 """
    f011 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s011 = Search (r'\d+', [f011], False, False, False)
    assert isinstance (s011.files, list)



def test_underline_is_not_a_bool_1 ():
    """ Test MAIN-012: files is not a bool 1 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f012 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f012], 0x007, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_underline_is_not_a_bool_2 ():
    """ Test MAIN-013: files is not a bool 2 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f013 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f013], [], False, False)
        assert pytest_wrapped_e.type == ValueError

def test_underline_is_not_a_bool_3 ():
    """ Test MAIN-014: files is not a bool 3 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f014 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f014], 'trustmeimanengineer', False, False)
        assert pytest_wrapped_e.type == ValueError

def test_underline_is_valid_1 ():
    """ Test MAIN-015: files is valid 1 """
    f015 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s015 = Search ("The quick brown fox*", [f015], True, False, False)
    assert s015.underline is True

def test_underline_is_valid_2 ():
    """ Test MAIN-016: files is valid 2 """
    f016 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s016 = Search (r'\d+', [f016], False, False, False)
    assert s016.underline is False



def test_color_is_not_a_bool_1 ():
    """ Test MAIN-017: color is not a bool 1 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f017 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f017], False, 0x007, False)
        assert pytest_wrapped_e.type == ValueError

def test_color_is_not_a_bool_2 ():
    """ Test MAIN-018: color is not a bool 2 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f018 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f018], False, [], False)
        assert pytest_wrapped_e.type == ValueError

def test_color_is_not_a_bool_3 ():
    """ Test MAIN-019: color is not a bool 3 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f019 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f019], True, 'trustmeimanengineer', False)
        assert pytest_wrapped_e.type == ValueError

def test_color_is_valid_1 ():
    """ Test MAIN-020: color is valid 1 """
    f020 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s020 = Search ("The quick brown fox*", [f020], False, True, False)
    assert s020.color is True

def test_color_is_valid_2 ():
    """ Test MAIN-021: color is valid 2 """
    f021 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s021 = Search (r'\d+', [f021], False, False, False)
    assert s021.color is False



def test_machine_is_not_a_bool_1 ():
    """ Test MAIN-022: machine is not a bool 1 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f022 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f022], False, False, 0x007)
        assert pytest_wrapped_e.type == ValueError

def test_machine_is_not_a_bool_2 ():
    """ Test MAIN-023: machine is not a bool 2 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f023 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f023], False, False, [])
        assert pytest_wrapped_e.type == ValueError

def test_machine_is_not_a_bool_3 ():
    """ Test MAIN-024: machine is not a bool 3 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f024 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f024], True, False, 'trustmeimanengineer')
        assert pytest_wrapped_e.type == ValueError

def test_machine_is_valid_1 ():
    """ Test MAIN-025: machine is valid 1 """
    f025 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s025 = Search ("The quick brown fox*", [f025], False, False, True)
    assert s025.machine is True

def test_machine_is_valid_2 ():
    """ Test MAIN-026: machine is valid 2 """
    f026 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s026 = Search (r'\d+', [f026], False, False, False)
    assert s026.machine is False



def test_mutual_exlusion_1 ():
    """ Test MAIN-027: mutual exclusion 1 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f027 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f027], True, True, True)
        assert pytest_wrapped_e.type == ValueError

def test_mutual_exlusion_2 ():
    """ Test MAIN-028: mutual exclusion 2 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f028 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f028], True, True, False)
        assert pytest_wrapped_e.type == ValueError

def test_mutual_exlusion_3 ():
    """ Test MAIN-029: mutual exclusion 3 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f029 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f029], True, False, True)
        assert pytest_wrapped_e.type == ValueError

def test_mutual_exlusion_4 ():
    """ Test MAIN-030: mutual exclusion 4 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        f030 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [f030], False, True, True)
        assert pytest_wrapped_e.type == ValueError

def test_mutual_exlusion_5 ():
    """ Test MAIN-031: mutual exclusion 5 """
    f031 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s031 = Search (r'\d+', [f031], False, False, False)
    assert s031.underline is False
    assert s031.color is False
    assert s031.machine is False

def test_mutual_exlusion_6 ():
    """ Test MAIN-032: mutual exclusion 6 """
    f032 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s032 = Search (r'\d+', [f032], True, False, False)
    assert s032.underline is True
    assert s032.color is False
    assert s032.machine is False

def test_mutual_exlusion_7 ():
    """ Test MAIN-033: mutual exclusion 7 """
    f033 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s033 = Search (r'\d+', [f033], False, True, False)
    assert s033.underline is False
    assert s033.color is True
    assert s033.machine is False

def test_mutual_exlusion_8 ():
    """ Test MAIN-034: mutual exclusion 8 """
    f034 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s034 = Search (r'\d+', [f034], False, False, True)
    assert s034.underline is False
    assert s034.color is False
    assert s034.machine is True



def test_files_do_not_exist_1 ():
    """ Test MAIN-035: a single file does not exist """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search (r'\d+', [], False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_files_do_not_exist_2 ():
    """ Test MAIN-036: two files do not exist """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search (r'\d+', ['', ''], False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_files_do_not_exist_3 ():
    """ Test MAIN-037: three files do not exist """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search (r'\d+', ['', 'LoremIpsum', ''], False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_files_do_exist_1 ():
    """ Test MAIN-038: one file that does exist """
    f038 = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    s038 = Search (r'\d+', [f038], False, False, False)
    assert s038.files[0].name == f038.name

def test_files_do_exist_2 ():
    """ Test MAIN-039: two files that do exist """
    f039a = tempfile.NamedTemporaryFile (delete = False, mode = 'r', prefix = 'search_test-')
    f039b = tempfile.NamedTemporaryFile (delete = False, mode = 'r', prefix = 'search_test-')

    f039a.close ()
    f039b.close ()

    tiow039a = open (f039a.name, 'r', encoding = "UTF-8")
    tiow039b = open (f039b.name, 'r', encoding = "UTF-8")

    s039 = Search (r'\d+', [tiow039a, tiow039b], False, False, False)

    assert s039.files[0].name == f039a.name
    assert s039.files[1].name == f039b.name

    os.unlink (f039a.name)
    os.unlink (f039b.name)

def test_files_do_exist_3 ():
    """ Test MAIN-040: three files that do exist """
    f040a = tempfile.NamedTemporaryFile (delete = False, mode = 'r', prefix = 'search_test-')
    f040b = tempfile.NamedTemporaryFile (delete = False, mode = 'r', prefix = 'search_test-')
    f040c = tempfile.NamedTemporaryFile (delete = False, mode = 'r', prefix = 'search_test-')

    f040a.close ()
    f040b.close ()
    f040c.close ()

    tiow040a = open (f040a.name, 'r', encoding = "UTF-8")
    tiow040b = open (f040b.name, 'r', encoding = "UTF-8")
    tiow040c = open (f040c.name, 'r', encoding = "UTF-8")

    s040 = Search (r'\d+', [tiow040a, tiow040b, tiow040c], False, False, False)

    assert s040.files[0].name == f040a.name
    assert s040.files[1].name == f040b.name
    assert s040.files[2].name == f040c.name

    os.unlink (f040a.name)
    os.unlink (f040b.name)
    os.unlink (f040c.name)

def test_files_some_do_exist ():
    """ Test MAIN-041: two files that do exist and one that does not exist """
    f041a = tempfile.NamedTemporaryFile (delete = False, mode = 'r', prefix = 'search_test-')
    f041c = tempfile.NamedTemporaryFile (delete = False, mode = 'r', prefix = 'search_test-')
    f041a.close ()
    f041c.close ()

    with pytest.raises (ValueError) as pytest_wrapped_e:
        tiow041a = open (f041a.name, 'r', encoding = "UTF-8")
        tiow041c = open (f041c.name, 'r', encoding = "UTF-8")
        s041 = Search (r'\d+', [tiow041a, '', tiow041c], False, False, False)
        tiow041a.close ()
        tiow041c.close ()
        assert s041.files[0].name == f041a.name
        assert s041.files[1] == ''
        assert s041.files[2].name == f041c.name
        assert pytest_wrapped_e.type == ValueError

    os.unlink (f041a.name)
    os.unlink (f041c.name)

def test_files_no_permissions ():
    """ Test MAIN-042: a single file with not the right permissions """
    f042 = tempfile.NamedTemporaryFile (delete = False, mode = 'r', prefix = 'search_test-')
    f042.close ()

    os.chmod (f042.name, 0)

    with pytest.raises (OSError) as pytest_wrapped_e:
        tiow042 = open (f042.name, 'r', encoding = "UTF-8")
        Search (r'\d+', [tiow042], False, False, False)
        tiow042.close ()
        assert pytest_wrapped_e.type == OSError

    os.unlink (f042.name)



def test_search_ok_1 (capsys):
    """ Test MAIN-043: search finishes succesfully 1 """
    s043 = Search (r'Lorem', [sample_100MB_file_with_text], False, False, False)
    s043.re_search ()
    s043.print_results ()

    captured_output        = capsys.readouterr ()
    expected_results       = open (sample_100MB_file_results.name, mode = 'r', encoding = 'ASCII')
    expected_results_text  = expected_results.read ()
    expected_results.close ()

    assert expected_results_text in captured_output.out

def test_search_ok_2 (capsys):
    """ Test MAIN-044: search finishes succesfully 2 """
    tiow044t = open (SAMPLE_SQL_FILE_WITH_TEXT, 'r', encoding = "UTF-8")
    tiow044r = open (SAMPLE_SQL_FILE_RESULTS,   'r', encoding = "UTF-8")

    s044 = Search (r'[dD]avid', [tiow044t], False, False, False)
    s044.re_search ()
    s044.print_results ()

    captured_output        = capsys.readouterr ()
    expected_results_text  = tiow044r.read ()

    assert expected_results_text in captured_output.out

def test_search_ok_3 (capsys):
    """ Test MAIN-045: search finishes succesfully 3 """
    tiow045t = open (SAMPLE_SQL_FILE_WITH_TEXT, 'r', encoding = "UTF-8")
    tiow045r = open (SAMPLE_SQL_FILE_RESULTS,   'r', encoding = "UTF-8")

    s045 = Search (r'\w?avid', [tiow045t], False, False, False)
    s045.re_search ()
    s045.print_results ()

    captured_output        = capsys.readouterr ()
    expected_results_text  = tiow045r.read ()

    assert expected_results_text in captured_output.out
