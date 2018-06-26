"""
idf-tags

Usage:
  idf-tags
  idf-tags [--recursive | -r | <idf_path>]
  idf-tags -h | --help
  idf-tags -v | --version

Options:
  -r --recursive    Search for IDF files is recursive (includes subdirectories)
  -h --help         Show this screen.
  -v --version      Show version.

Examples:
  idf-tags          Generates a tag file for all files in current directory
  idf-tags -r       Tag file including subdirectories
  idf-tags in.idf   Tag file for a specific IDF file

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/jmarrec/idf-tags
"""


from docopt import docopt
from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    from idftags.idf_tag import tag_idfs
    options = docopt(__doc__, version=VERSION)

    # Call the tagged with the right options
    if options['<idf_path>']:
        tag_idfs(idf_path=options['<idf_path>'])
    else:
        tag_idfs(recursive=options['--recursive'])
