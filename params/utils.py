#!/usr/bin/env python
# coding: utf-8

import sys
import json
import copy


PY3 = sys.version_info >= (3,)

if PY3:
    unicode_type = str
    basestring_type = str
else:
    # The names unicode and basestring don't exist in py3 so silence flake8.
    unicode_type = unicode  # noqa
    basestring_type = basestring  # noqa


_TO_UNICODE_TYPES = (unicode_type, type(None))


def to_unicode(value):
    """Converts a string argument to a unicode string.

    If the argument is already a unicode string or None, it is returned
    unchanged.  Otherwise it must be a byte string and is decoded as utf8.
    """
    if isinstance(value, _TO_UNICODE_TYPES):
        return value
    if not isinstance(value, bytes):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value)
        )
    return value.decode("utf-8")


def _copy_dict(x, memo):
    y = {}
    memo[id(x)] = y
    for key, value in x.iteritems():
        y[key] = unicode_copy(value, memo)
    return y


def _copy_list(x, memo):
    y = []
    memo[id(x)] = y
    for a in x:
        y.append(unicode_copy(a, memo))
    return y


def unicode_copy(x, memo=None, _nil=[]):
    if memo is None:
        memo = {}

    d = id(x)
    y = memo.get(d, _nil)
    if y is not _nil:
        return y

    if isinstance(x, dict):
        y = _copy_dict(x, memo)
    elif isinstance(x, list):
        y = _copy_list(x, memo)
    elif isinstance(x, str):
        y = to_unicode(x)
    else:
        y = x

    memo[d] = y
    copy._keep_alive(x, memo)  # Make sure x lives at least as long as d
    return y


_BASESTRING_TYPES = (basestring_type, type(None))


def to_basestring(value):
    """Converts a string argument to a subclass of basestring.

    In python2, byte and unicode strings are mostly interchangeable,
    so functions that deal with a user-supplied argument in combination
    with ascii string constants can use either and should return the type
    the user supplied.  In python3, the two types are not interchangeable,
    so this method is needed to convert byte strings to unicode.
    """
    if isinstance(value, _BASESTRING_TYPES):
        return value
    if not isinstance(value, bytes):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value)
        )
    return value.decode("utf-8")


def json_decode(value):
    """Returns Python objects for the given JSON string."""
    return json.loads(to_basestring(value))


def is_empty_string(v):
    if v == '' or v == u'':
        return True
    return False
