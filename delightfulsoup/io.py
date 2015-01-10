"""
utils.common
=====


"""

import bs4 as _bs4
import json as _json
import os as _os

# -------------------------------------------------------------------------------


def load_soup(path_html):
    """
    """
    with open(path_html, 'r') as f:
        return _bs4.BeautifulSoup(f)


def dump_soup(soup, path_html,
              overwrite=True,
              pretty=True, encoding='utf-8',
              remove_tag=False):
    """
    """

    if pretty:
        soup_str = str(soup.prettify().encode(encoding))
    else:
        soup_str = str(soup.encode(encoding))

    if remove_tag and isinstance(remove_tag, str):
        soup_str = soup_str.replace('<{tag}>'.format(tag=remove_tag), '')
        soup_str = soup_str.replace('</{tag}>'.format(tag=remove_tag), '')

    with open(path_html, 'wb') as f:
        f.write(soup_str.strip())


def load_json(path_json):
    """
    """

    with open(path_json, 'r') as f:
        return _json.load(f)


def dump_json(json, path_json, indent=4):
    """
    """
    with open(path_json, 'wb') as f:
        _json.dump(json, f, indent=indent)
        f.write("\n")


# add http://www.lifl.fr/~riquetd/parse-a-json-file-with-comments.html
