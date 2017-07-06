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

from dpp import expected

import pytest


class A(object):
    lazy_value = expected.Expected(predicate=lambda x: isinstance(x, str),
                                   exc_cls=TypeError,
                                   message='\'{value}\' is not of type \'str\'',
                                   trigger_on_set=False)

    greedy_value = expected.Expected(predicate=lambda x: isinstance(x, str),
                                     exc_cls=TypeError,
                                     message='\'{value}\' is not of type \'str\'',
                                     trigger_on_set=True)


def test_expected():
    a = A()
    a.lazy_value = 'hello'
    v = a.lazy_value
    assert v == 'hello'
    assert isinstance(v, str)

    a.lazy_value = 1
    with pytest.raises(TypeError):
        v = a.lazy_value

    a.greedy_value = 'hello'
    v = a.greedy_value
    assert v == 'hello'
    assert isinstance(v, str)

    with pytest.raises(TypeError):
        a.greedy_value = 1

    try:
        a.greedy_value = 1
    except TypeError:
        v = a.greedy_value
        assert v == 'hello'
        assert isinstance(v, str)
