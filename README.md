# Yet another simple grep implementation

This repository contains my implementation for a simple grep-like tool based in Python: a Python3 script which searches for a pattern using a regular expression in lines of text, and prints the lines which contain matching text. The script's output format should be:

    file_name line_number line

## My approach to this implementation
At first, I wrote dozens of tests to make sure that the command-line parameters were correctly parsed and consistent, so I could confidentially test the output knowing that no wrong input (up to an extent, of course) could mess up with the results (a kind of Test Driven Development approach).

From there, I kept on evolving and improving the code as I kept on implementing additional parameters and options, as well as some bug fixing, of course.

## Prerequisites
This tool relies on standard Python packages and libraries. Assuming you have a working Python3 installation in a computer (currently Python 3.8.10 in my case):

1. Optionally install the virtualenv package:
    * For Debian-based OS: `sudo apt install --assume-yes python3-virtualenv`
    * For RHEL-based OS: `sudo yum install --assumeyes python3-virtualenv`

1. Use the virtual environment, if installed (see the previous step):

    ```
    virtualenv basic-grep
    source basic-grep/bin/activate
    ```

1. Make sure you upgrade pip and install the requisites:

    ```
    python3 -m pip install --upgrade pip
    pip install pep8 pylint pytest numpy
    ```

1. Done!

## Assumptions

* For the sake of simplicity, I have assumed that every input or output stream or file is ASCII-based, so no dealing with different encodings.
* Multiple matches on a single line are allowed without overlapping.
* This script is meant to be executed on standard Linux distributions.
* This script adheres to [Python's PEP8 style guide](https://pep8.org/).

## Additional considerations

* Implicit closing files are "used" when possible.
* The mutually exclusive parameters from the command-line are parsed in the same order as declared.

# Improvement areas and pending tasks

* The `re_search ()` from the `Search` class may be improved for not having similar code for string (the standard input stream) and list arguments.
* Unit tests for the parameters `underline`, `colo` and `machine`: they have been deliberately left out of this first iteration due to timing issues.
* A few tests like the one named `test_files_no_permissions ()` from the `Search` test program `search_test.py` use the [module tempfile](https://docs.python.org/3.9/library/tempfile.html) and open the same file twice without closing it first; it would be necessary to close it before opening again, and calling the temporary file creator with the parameter `delete = False`). The reason being that according to the module documentation (see the link from above):

    >  Whether the name can be used to open the file a second time, while the named temporary file is still open, varies across platforms (it can be so used on Unix; it cannot on Windows NT or later).

* I dropped the _stdin_ automated tests because [the `pytest` framework redirects the standard input stream to NULL](https://pytest.org/en/7.1.x/how-to/capture-stdout-stderr.html#default-stdout-stderr-stdin-capturing-behaviour
) and [it is harder to bypass this](https://pytest.org/en/7.1.x/how-to/monkeypatch.html); this is out of the current development iteration.

* **IN PROGRESS** in the branch `print_once_lines_with_multiple_occurences`: print once a line with multiple occurrences of a match; see [commit 4ae6ef5 from that branch])(https://github.com/jordibellido/python-basic-grep/commit/4ae6ef59f1663d0623f3bb8f678d4935ee4f377d) for additional information on this. At first I thought on using a more elaborated data structure like a hash of arrays of hashes, but it ended up being way too much complex for what this implementation is meant for.

## Performance
The slowest test from the `search_test.py` test suite is the one named `test_search_ok_1`, as it processes and search for strings a 100 MB file. According to `pytest`, it takes slightly more than 1 second to finish this test:

    $ python3 -m pytest search_test.py --durations=3 -vvv
        [...]
    ====================== slowest 3 durations ======================
    1.20s call     search_test.py::test_search_ok_1
    0.00s call     search_test.py::test_search_ok_3
    0.00s call     search_test.py::test_search_ok_2
