# -*- coding: utf-8 -*-
#
# Copyright 2016 Massimiliano Culpo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Convenience tools to manipulate python objects
"""

import re

_IS_SPECIAL_PATTERN = re.compile('__[^_]+__')


def is_special(item):
    """
    Returns True if the item is a special function or method, False otherwise

    :param item: item to be inspected
    :return: True or False
    """
    # TODO : this matches any __<name>__ not only special methods
    name = getattr(item, '__name__')
    if _IS_SPECIAL_PATTERN.match(name):
        return True
    return False


def is_private(item):
    """
    Returns True if the item is 'private', False otherwise

    :param item: item to be inspected
    :return: True or False
    """
    name = getattr(item, '__name__')
    if name.startswith('_') and not is_special(item):
        return True
    return False
