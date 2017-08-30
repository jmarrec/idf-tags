"""Tests for our main idf-tags CLI module."""

import sys
import os
import glob as gb
from subprocess import check_output, Popen, PIPE, STDOUT
import pytest

from idftags import __version__ as VERSION

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestHelp():
    """
    Py.test class for the help
    """
    def test_help(self):
        """
        Py.test for -h or --help
        """
        output = check_output(['idf-tags', '-h'])
        assert 'Usage:' in output.decode('utf-8')

        output = check_output(['idf-tags', '--help'])
        assert 'Usage:' in output.decode('utf-8')

    def test_recursive_and_path(self):
        """
        Py.test to check that if both --recursive and a path are given it
        shows the help
        """
        # Cannot call check_output, it's going to crash because the return code
        # isn't 0 in this case (it is - after all - a non valid call!)
        output = Popen(['idf-tags', '-r', 'i.idf'],
                       stdout=PIPE, stderr=STDOUT).communicate()[0]
        assert 'Usage:' in output.decode('utf-8')

        output = Popen(['idf-tags', '--recursive', 'i.idf'],
                       stdout=PIPE, stderr=STDOUT).communicate()[0]
        assert 'Usage:' in output.decode('utf-8')


class TestVersion():
    """
    Py.test class for version
    """
    def test_version_short(self):
        """
        Py.test for -v
        """
        output = check_output(['idf-tags', '-v'])
        assert output.decode('utf-8').strip() == VERSION

    def test_version_long(self):
        """
        Py.test for --version
        """
        output = check_output(['idf-tags', '--version'])
        assert output.decode('utf-8').strip() == VERSION


class TestIdfTagsCLI():
    """
    Py.test class to test that the arguments are understood correctly by the
    CLI
    """

    @pytest.fixture(autouse=True)
    def cleanup_out_files(self):
        """
        Fixture run around tests. Will change the current working dir
        Will delete all 'xx-out.idf' files created to avoid multiplication
        of files.
        """

        curdir = os.getcwd()
        os.chdir("{}/test_files".format(TEST_DIR))

        yield

        # This runs even if the test failed
        # Python 2 doesn't support recursive...
        if sys.version_info[0] < 3:
            # Python 2 doesn't support recursive...
            import fnmatch
            for root, dirnames, filenames in os.walk('.'):
                for filename in fnmatch.filter(filenames, '*out.idf'):
                    idf_path = os.path.join(root, filename)
                    os.remove(idf_path)
        else:
            for filepath in gb.iglob("**/*out.idf", recursive=True):
                os.remove(filepath)

        # Teardown
        os.chdir(curdir)

    def test_without_recursive(self):
        """
        Py.test when recursive isn't used
        """
        output = check_output(['idf-tags']).decode('utf-8')
        lines = output.split('\n')
        assert len(lines) == 4

    def test_with_recursive(self):
        """
        Py.test when recursive is used
        """
        output = check_output(['idf-tags', '-r']).decode('utf-8')
        lines = output.split('\n')
        assert len(lines) == 5

    def test_with_path(self):
        """
        Py.test for a single file
        """
        output = check_output(['idf-tags',
                               'WaterHeaterStandAlone.idf']).decode('utf-8')
        lines = output.split('\n')
        # There's an extra newline character line... user sees two
        # Processing xxxx.idf and "Generated tag"
        assert len(lines) == 3
