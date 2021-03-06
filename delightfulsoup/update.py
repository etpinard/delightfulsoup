"""
update
======


"""
import bs4 as _bs4

import utils.shortcuts as _shc

# -------------------------------------------------------------------------------


def add_attr(node, attr_dict):
    """
    """

    # ...
    if not isinstance(attr_dict, dict):
        raise Exception('')
    if len(attr_dict.keys()) != 1:
        raise Exception('')

    # ...
    astr = attr_dict.keys()[0]
    attrs = attr_dict[astr]

    # ...
    if not isinstance(attrs, list):
        attrs = [attrs]

    #
    try:
        attr_current = node[astr]
    except KeyError:
        attr_current = None

    #
    for attr in attrs:
        if attr_current is None:
            node[astr] = attr
        elif attr not in attr_current:
            node[astr] = ' - '.join([attr_current, attr])


def insert_inside_nodes(nodes, tag,
                        node_attrs={},
                        tag_attrs={}, tag_content='',
                        replace=True, no_empty=True):
    """
    """

    if not isinstance(nodes, list):
        raise Exception("Positional argument 1 'nodes' must be a list")
    if not isinstance(tag, str):
        raise Exception("Positional argument 2 'tag' must be a str")
    if not isinstance(node_attrs, dict):
        raise Exception("Argument 'node_attr' must be a dict")
    if not isinstance(tag_attrs, dict):
        raise Exception("Argument 'tag_attr' must be a dict")

    for node in nodes:

        # Add attr to node
        for astr, aval in node_attrs.items():
            _aval = _shc.call_or_get(aval, node)
            if _aval:
                node[astr] = _aval

        # Link tag attrs to tmp dict
        _tag_attrs = dict()
        for astr, aval in tag_attrs.items():
            _aval = _shc.call_or_get(aval, node)
            if _aval:
                _tag_attrs[astr] = _aval

        # Link tag content to tmp var
        _tag_content = _shc.call_or_get(tag_content, node)

        # _insert_tag does the rest
        _shc._insert_tag(node, tag, _tag_attrs, _tag_content,
                         replace, no_empty)


def insert_around_nodes(nodes, tag,
                        node_attrs={}, tag_attrs={}):
    """
    """

    if not isinstance(nodes, list):
        raise Exception("Positional argument 1 'nodes' must be a list")
    if not isinstance(tag, str):
        raise Exception("Positional argument 2 'tag' must be a str")
    if not isinstance(node_attrs, dict):
        raise Exception("Argument 'node_attr' must be a dict")
    if not isinstance(tag_attrs, dict):
        raise Exception("Argument 'tag_attr' must be a dict")

    for node in nodes:

        # Add attr to node
        for astr, aval in node_attrs.items():
            _aval = _shc.call_or_get(aval, node)
            if _aval:
                node[astr] = _aval

        # Link tag attrs to tmp dict
        _tag_attrs = dict()
        for astr, aval in tag_attrs.items():
            _aval = _shc.call_or_get(aval, node)
            if _aval:
                _tag_attrs[astr] = _aval

        # _wrap_tag does the rest
        _shc._wrap_tag(node, tag, _tag_attrs)


def strip_nodes(soup, nodes_to_rm):

    for node_to_rm in nodes_to_rm:
        for node in soup.findAll(node_to_rm):
            node.extract()


def strip_attrs(soup, *args):
    """
    """

    # List of all 'deletable' attributes
    # (i.e. no 'href' or iframe attributes)
    ALL_ATTRS = ["class", "id", "name", "style",
                 "colspan", "rowspan",
                 "cellpadding", "cellspacing",
                 "tabindex"]

    try:
        attrs = args[0]
    except:
        attrs = ALL_ATTRS

    for attr in attrs:
        del soup[attr]

    for tag in soup():
        for attr in attrs:
            del tag[attr]
