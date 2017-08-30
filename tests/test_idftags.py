"""Tests for our `idftags` program with good arguments."""

import os
# import glob as gb

import pytest

from idftags.idf_tag import lint_and_tag_file, tag_idfs
from idftags.idf_tag import find_non_reference_classes, NOT_REFERENCE_CLASSES


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir("{}/test_files".format(TEST_DIR))


class TestIdfTags():
    """
    Py.test class for the idf_tag
    """
    def test_lint_and_tag_file(self):
        """
        Py.test for the main function to lint and tag a single IDF file
        """
        idf_path = 'WaterHeaterStandAlone.idf'
        # Check you have tags
        tags = lint_and_tag_file(idf_path)
        assert tags
        # And it's the correct format
        for tag in tags:
            assert len(tag.split('\t')) == 3

            name, filepath, regex = tag.split('\t')

            # The first is a Name, shouldn't have any spaces
            assert ' ' not in name

            # The second is an idf file
            assert os.path.splitext(filepath)[1] == '.idf'

            # the third is a regex
            assert regex[:2] == '/^'
            assert regex[-1] == '$'

        # Check the linted file was created
        path, ext = os.path.splitext(idf_path)
        out_file = "{}-out{}".format(path, ext)
        assert os.path.isfile(out_file)

        # TODO: check that the names where properly replaced in the out.idf

        # Remove it
        os.remove(out_file)

    def test_not_ref_class_up_to_date(self):
        """
        Py.test to check that the non reference classes hardcoded as still up
        to date with the current IDD
        """
        # This is only going to run on my system...
        idd_path = 'Energy+.idd'
        idd_not_ref_classes = find_non_reference_classes(idd_path)
        assert idd_not_ref_classes == NOT_REFERENCE_CLASSES

    def test_tags_idf_not_idf(self):
        """
        Py.test to check that it will raise if the file isn't an idf
        """
        with pytest.raises(ValueError):
            tag_idfs('afile')

    def test_tags_idf_bad_idf(self):
        """
        Py.test to check that it will raise if the file isn't a valid file
        """
        with pytest.raises(IOError):
            tag_idfs('nonexisting.idf')
