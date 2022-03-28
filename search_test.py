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
with open (sample_100MB_file_with_text.name, 'w', encoding = 'ASCII') as fout:
    text_file = open ('data/sample01.txt', 'r', encoding = 'ASCII')
    fout.write (text_file.read () * (100 * 1024))
    text_file.close ()

# Generate the search result for a known regexp for the sample file:
with open (f'{sample_100MB_file_results.name}', 'w', encoding = 'ASCII') as fout:
    fout.write (f"{sample_100MB_file_with_text.name} 0 Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec venenatis velit ac enim tristique faucibus. Proin dapibus arcu eget massa convallis posuere malesuada vel sapien.\n")
    for current_line in range (10, ((100 * 1024) - 1), 10):
        fout.write (f"{sample_100MB_file_with_text.name} {current_line} Morbi tempor neque vel convallis commodo. Phasellus velit lacus, accumsan sed dolor eget, egestas faucibus nisl. In vel velit purusLorem ipsum dolor sit amet, consectetur adipiscing elit. Donec venenatis velit ac enim tristique faucibus. Proin dapibus arcu eget massa convallis posuere malesuada vel sapien.\n")



##### SAMPLE FILE 02
SAMPLE_SQL_FILE_WITH_TEXT = 'data/sample02.sql'
SAMPLE_SQL_FILE_RESULTS   = 'data/result02.txt'



##### 0. DOUBLE CHECK THE GENERATION OF THE TEST TEXT FILES
def test_generated_files ():
    """ Test MAIN-000: test generated files sizes """
    # SAMPLE FILES 01
    assert os.path.getsize (sample_100MB_file_with_text.name) == (100 * 1024 * 1024)

    # There are (100 * 1024) occurences of the Lorem word, which is 11-char long,
    # plus the starting and closing bracket, minus the last comma and space
    # (which are not necessary): (100 * 11 * 1024) + 2 - 1 - 1
    assert os.path.getsize (sample_100MB_file_results.name) == 3480598

    # SAMPLE FILES 02
    assert os.path.getsize (SAMPLE_SQL_FILE_WITH_TEXT) == 86561
    assert os.path.getsize (SAMPLE_SQL_FILE_RESULTS)   == 12538



##### 1. ESSENTIAL FUNCTIONAL TESTS
def test_search_ok_1 (capsys):
    """ Search finishes succesfully 1 """
    tiow = open (sample_100MB_file_with_text.name, 'r', encoding = "UTF-8")
    search = Search (r'Lorem', [tiow], False, False, False)
    search.re_search ()
    search.print_results ()

    captured_output        = capsys.readouterr ()
    expected_results       = open (sample_100MB_file_results.name, mode = 'r', encoding = 'ASCII')
    expected_results_text  = expected_results.read ()
    expected_results.close ()

    assert expected_results_text in captured_output.out

def test_search_ok_2 (capsys):
    """ Search finishes succesfully 2 """
    tiowt = open (SAMPLE_SQL_FILE_WITH_TEXT, 'r', encoding = "UTF-8")
    tiowr = open (SAMPLE_SQL_FILE_RESULTS,   'r', encoding = "UTF-8")

    search = Search (r'[dD]avid', [tiowt], False, False, False)
    search.re_search ()
    search.print_results ()

    captured_output        = capsys.readouterr ()
    expected_results_text  = tiowr.read ()

    assert expected_results_text in captured_output.out

def test_search_ok_3 (capsys):
    """ Search finishes succesfully 3 """
    tiowt = open (SAMPLE_SQL_FILE_WITH_TEXT, 'r', encoding = "UTF-8")
    tiowr = open (SAMPLE_SQL_FILE_RESULTS,   'r', encoding = "UTF-8")

    search = Search (r'\w?avid', [tiowt], False, False, False)
    search.re_search ()
    search.print_results ()

    captured_output        = capsys.readouterr ()
    expected_results_text  = tiowr.read ()

    assert expected_results_text in captured_output.out

def test_search_ok_4 (capsys):
    """ Search finishes succesfully 4 - no results """
    tiowt = open (SAMPLE_SQL_FILE_WITH_TEXT, 'r', encoding = "UTF-8")

    search = Search (r'0123456789', [tiowt], False, False, False)
    search.re_search ()
    search.print_results ()

    captured_output        = capsys.readouterr ()

    assert len (captured_output.out) == 0
    assert captured_output.out       == ''



##### 2. ADDITIONAL SEARCH TESTS
def test_files_do_not_exist_1 ():
    """ A single file does not exist """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search (r'\d+', [], False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_files_do_not_exist_2 ():
    """ Two files do not exist """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search (r'\d+', ['', ''], False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_files_do_not_exist_3 ():
    """ Three files do not exist """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search (r'\d+', ['', 'LoremIpsum', ''], False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_files_do_exist_1 ():
    """ One file that does exist """
    file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    search = Search (r'\d+', [file_d], False, False, False)
    assert search.files[0].name == file_d.name

def test_files_do_exist_2 ():
    """ Two files that do exist """
    file_d_01 = tempfile.NamedTemporaryFile (delete = False, mode = 'r', prefix = 'search_test-')
    file_d_02 = tempfile.NamedTemporaryFile (delete = False, mode = 'r', prefix = 'search_test-')

    file_d_01.close ()
    file_d_02.close ()

    tiow_01 = open (file_d_01.name, 'r', encoding = "UTF-8")
    tiow_02 = open (file_d_02.name, 'r', encoding = "UTF-8")
    search  = Search (r'\d+', [tiow_01, tiow_02], False, False, False)

    assert search.files[0].name == file_d_01.name
    assert search.files[1].name == file_d_02.name

    os.unlink (file_d_01.name)
    os.unlink (file_d_02.name)

def test_files_do_exist_3 ():
    """ Three files that do exist """
    file_d_01 = tempfile.NamedTemporaryFile (delete = False, mode = 'r', prefix = 'search_test-')
    file_d_02 = tempfile.NamedTemporaryFile (delete = False, mode = 'r', prefix = 'search_test-')
    file_d_03 = tempfile.NamedTemporaryFile (delete = False, mode = 'r', prefix = 'search_test-')

    file_d_01.close ()
    file_d_02.close ()
    file_d_03.close ()

    tiow_01 = open (file_d_01.name, 'r', encoding = "UTF-8")
    tiow_02 = open (file_d_02.name, 'r', encoding = "UTF-8")
    tiow_03 = open (file_d_03.name, 'r', encoding = "UTF-8")
    search  = Search (r'\d+', [tiow_01, tiow_02, tiow_03], False, False, False)

    assert search.files[0].name == file_d_01.name
    assert search.files[1].name == file_d_02.name
    assert search.files[2].name == file_d_03.name

    os.unlink (file_d_01.name)
    os.unlink (file_d_02.name)
    os.unlink (file_d_03.name)

def test_files_some_do_exist ():
    """ Two files that do exist and one that does not exist """
    file_d_01 = tempfile.NamedTemporaryFile (delete = False, mode = 'r', prefix = 'search_test-')
    file_d_02 = tempfile.NamedTemporaryFile (delete = False, mode = 'r', prefix = 'search_test-')
    file_d_01.close ()
    file_d_02.close ()

    with pytest.raises (ValueError) as pytest_wrapped_e:
        tiow_01 = open (file_d_01.name, 'r', encoding = "UTF-8")
        tiow_02 = open (file_d_02.name, 'r', encoding = "UTF-8")
        search  = Search (r'\d+', [tiow_01, '', tiow_02], False, False, False)

        tiow_01.close ()
        tiow_02.close ()

        assert search.files[0].name == tiow_01.name
        assert search.files[1] == ''
        assert search.files[2].name == tiow_02.name
        assert pytest_wrapped_e.type == ValueError

    os.unlink (tiow_01.name)
    os.unlink (tiow_02.name)

def test_files_no_permissions ():
    """ A single file with not the right permissions """
    file_d = tempfile.NamedTemporaryFile (delete = False, mode = 'r', prefix = 'search_test-')
    file_d.close ()

    os.chmod (file_d.name, 0)

    with pytest.raises (OSError) as pytest_wrapped_e:
        tiow = open (file_d.name, 'r', encoding = "UTF-8")
        Search (r'\d+', [tiow], False, False, False)
        tiow.close ()
        assert pytest_wrapped_e.type == OSError

    os.unlink (file_d.name)



##### 3. TESTS FOR THE SEARCH CLASS
def test_regex_is_empty ():
    """ Regex is empty """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search ('', [], False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_regex_is_not_valid ():
    """ Regex is not valid """
    with pytest.raises (RuntimeError) as pytest_wrapped_e:
        Search ('[*', [], False, False, False)
        assert pytest_wrapped_e.type == RuntimeError

def test_regex_is_not_an_string_1 ():
    """ Regex is not an string 1 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search ({}, [], False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_regex_is_not_an_string_2 ():
    """ Regex is not an string 2 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search (3.1415926535, [], False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_regex_is_valid_1 ():
    """ Regex is valid 1 """
    file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    Search ("The quick brown fox*", [file_d], False, False, False)

def test_regex_is_valid_2 ():
    """ Regex is valid 2 """
    file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    Search (r'\d+', [file_d], False, False, False)



def test_files_is_empty ():
    """ Parameter files is empty """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search (r'\d+', [], False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_files_is_not_a_list_1 ():
    """ Parameter files is not a list 1 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search (r'\d+', '', False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_files_is_not_a_list_2 ():
    """ Parameter files is not a list 2 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        Search (r'\d+', 1.6180339887, False, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_files_is_valid_1 ():
    """ Parameter files is valid 1 """
    file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    search = Search ("The quick brown fox*", [file_d], False, False, False)
    assert isinstance (search.files, list)

def test_files_is_valid_2 ():
    """ Parameter files is valid 2 """
    file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    search = Search (r'\d+', [file_d], False, False, False)
    assert isinstance (search.files, list)



def test_underline_is_not_a_bool_1 ():
    """ Parameter underline is not a bool 1 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [file_d], 0x007, False, False)
        assert pytest_wrapped_e.type == ValueError

def test_underline_is_not_a_bool_2 ():
    """ Parameter underline is not a bool 2 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [file_d], [], False, False)
        assert pytest_wrapped_e.type == ValueError

def test_underline_is_not_a_bool_3 ():
    """ Parameter underline is not a bool 3 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [file_d], 'trustmeimanengineer', False, False)
        assert pytest_wrapped_e.type == ValueError

def test_underline_is_valid_1 ():
    """ Parameter underline is valid 1 """
    file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    search = Search ("The quick brown fox*", [file_d], True, False, False)
    assert search.underline is True

def test_underline_is_valid_2 ():
    """ Parameter underline is valid 2 """
    file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    search = Search (r'\d+', [file_d], False, False, False)
    assert search.underline is False



def test_color_is_not_a_bool_1 ():
    """ Parameter color is not a bool 1 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [file_d], False, 0x007, False)
        assert pytest_wrapped_e.type == ValueError

def test_color_is_not_a_bool_2 ():
    """ Parameter color is not a bool 2 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [file_d], False, [], False)
        assert pytest_wrapped_e.type == ValueError

def test_color_is_not_a_bool_3 ():
    """ Parameter color is not a bool 3 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [file_d], True, 'trustmeimanengineer', False)
        assert pytest_wrapped_e.type == ValueError

def test_color_is_valid_1 ():
    """ Parameter color is valid 1 """
    file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    search = Search ("The quick brown fox*", [file_d], False, True, False)
    assert search.color is True

def test_color_is_valid_2 ():
    """ Parameter color is valid 2 """
    file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    search = Search (r'\d+', [file_d], False, False, False)
    assert search.color is False



def test_machine_is_not_a_bool_1 ():
    """ Parameter machine is not a bool 1 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [file_d], False, False, 0x007)
        assert pytest_wrapped_e.type == ValueError

def test_machine_is_not_a_bool_2 ():
    """ Parameter machine is not a bool 2 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [file_d], False, False, [])
        assert pytest_wrapped_e.type == ValueError

def test_machine_is_not_a_bool_3 ():
    """ Parameter machine is not a bool 3 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [file_d], True, False, 'trustmeimanengineer')
        assert pytest_wrapped_e.type == ValueError

def test_machine_is_valid_1 ():
    """ Parameter machine is valid 1 """
    file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    search = Search ("The quick brown fox*", [file_d], False, False, True)
    assert search.machine is True

def test_machine_is_valid_2 ():
    """ Parameter machine is valid 2 """
    file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    search = Search (r'\d+', [file_d], False, False, False)
    assert search.machine is False



def test_mutual_exlusion_1 ():
    """ Mutual exclusion 1 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [file_d], True, True, True)
        assert pytest_wrapped_e.type == ValueError

def test_mutual_exlusion_2 ():
    """ Mutual exclusion 2 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [file_d], True, True, False)
        assert pytest_wrapped_e.type == ValueError

def test_mutual_exlusion_3 ():
    """ Mutual exclusion 3 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [file_d], True, False, True)
        assert pytest_wrapped_e.type == ValueError

def test_mutual_exlusion_4 ():
    """ Mutual exclusion 4 """
    with pytest.raises (ValueError) as pytest_wrapped_e:
        file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
        Search (r'\d+', [file_d], False, True, True)
        assert pytest_wrapped_e.type == ValueError

def test_mutual_exlusion_5 ():
    """ Mutual exclusion 5 """
    file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    search = Search (r'\d+', [file_d], False, False, False)
    assert search.underline is False
    assert search.color is False
    assert search.machine is False

def test_mutual_exlusion_6 ():
    """ Mutual exclusion 6 """
    file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    search = Search (r'\d+', [file_d], True, False, False)
    assert search.underline is True
    assert search.color is False
    assert search.machine is False

def test_mutual_exlusion_7 ():
    """ Mutual exclusion 7 """
    file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    search = Search (r'\d+', [file_d], False, True, False)
    assert search.underline is False
    assert search.color is True
    assert search.machine is False

def test_mutual_exlusion_8 ():
    """ Mutual exclusion 8 """
    file_d = tempfile.NamedTemporaryFile (mode = 'r', prefix = 'search_test-')
    search = Search (r'\d+', [file_d], False, False, True)
    assert search.underline is False
    assert search.color is False
    assert search.machine is True
