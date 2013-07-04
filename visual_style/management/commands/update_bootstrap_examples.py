import os
import os.path
import re

from cssselect import HTMLTranslator
from django.core.management.base import BaseCommand, CommandError
import lxml.etree
import lxml.html


EXTRACTED_SELECTORS = ('h1, h2, h3, h4, h5, h6, '
                       '.bs-docs-example, #buttons table')

HEADER_NESTING = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6')


def is_header(tag):
    """Returns True if a tag is a header tag, False otherwise"""
    return tag in HEADER_NESTING


def get_tag_nesting(tag):
    """Returns the nesting level of a tag, where smaller levels are outside"""
    try:
        return HEADER_NESTING.index(tag)
    except ValueError:
        return len(HEADER_NESTING)


def filter_nonexample_headers(elements):
    """Converts a flat list of header and example elements into a list
    with one (meaningful) header per example in the list. As a rule
    of thumb, all headers starting with "Example" are considered
    too vague to be helpful, and are replaced with the preceding top-level
    header.

    """

    filtered_elements = []
    last_tag = None

    for element in elements[::-1]:
        tag = element.tag
        is_example = not is_header(tag)

        if last_tag is None:
            is_parent = False
        else:
            is_parent = get_tag_nesting(tag) < get_tag_nesting(last_tag)

        if is_example or is_parent:
            filtered_elements.append(element)
            last_tag = tag

    return filtered_elements[::-1]


def rewrite_asset_urls(html):
    """Rewrites asset URLs in the bootstrap documentation to use appropriate
    static file lookup, instead of hardcoding the relative URLs.

    """

    asset_url_regex = re.compile(r'"(assets/[^"]*)"')
    replacement = r'"{% static "bower/bootstrap/docs/\1" %}"'
    return re.sub(asset_url_regex, replacement, html)


def generate_examples_from_file(file_path):
    """Extracts a list of strings representing header and example elements
    from the file specifed by `file_path`.

    """

    expression = HTMLTranslator().css_to_xpath(EXTRACTED_SELECTORS)
    document = lxml.html.parse(file_path)
    elements = document.xpath(expression)

    for el in filter_nonexample_headers(elements):
        html = lxml.etree.tostring(el, pretty_print=True, method='html')
        yield rewrite_asset_urls(html)


def extract_examples_from_directory(directory_path):
    """Extracts a single string containing all of the header and example
    elements for all HTML files (determined by possession of a '.html' suffix)
    found in the directory specified by `directory_path`.

    This function does not recurse into subdirectories.

    """

    chunks = ['{% load static %}']
    for filename in os.listdir(directory_path):
        # Please don't suffix directory names with .html :-)
        if filename.endswith('.html'):
            file_path = os.path.join(directory_path, filename)
            chunk = generate_examples_from_file(file_path)
            chunks.extend(chunk)
    return '\n'.join(chunks)


def get_bootstrap_doc_directory_path():
    """Returns the path to the bootstrap documentation directory"""

    doc_dir_name = os.path.join('static', 'bower', 'bootstrap', 'docs')

    for dir_path, dir_names, filenames in os.walk("."):
        for dir_name in dir_names:
            subdir_path = os.path.join(dir_path, dir_name)
            if subdir_path.endswith(doc_dir_name):
                return subdir_path

    return None


def up_directories(path, count=0):
    """Returns the parent directory of a file. If the optional `count`
    parameter is specified, then the `count`th grandparent directory will
    be returned.

    """

    for _ in range(count + 1):
        path = os.path.dirname(path)

    return path


def get_output_path():
    """Returns the path to the file that will hold the collected examples."""

    # We're in visual_style/management/commands/foo.py, so we want to be
    #  two directories up
    visual_style_path = up_directories(__file__, count=2)
    snippet_dirname = os.path.join("templates", "visual_style", "snippets")
    snippet_directory = os.path.join(visual_style_path, snippet_dirname)
    return os.path.join(snippet_directory, "bootstrap.html")


class Command(BaseCommand):
    help = 'Updates the bootstrap examples in the visual_style app'

    def handle(self, *args, **kwargs):
        input_directory_path = get_bootstrap_doc_directory_path()
        output_file_path = get_output_path()

        if input_directory_path is None:
            # XXX: Make this error more helpful
            raise CommandError('Could not find bootstrap doc directory')

        example_html = extract_examples_from_directory(input_directory_path)

        with open(output_file_path, "w") as f:
            f.write(example_html)

        self.stdout.write('OK -- wrote %d bytes to %s' %
                          (len(example_html), output_file_path))
