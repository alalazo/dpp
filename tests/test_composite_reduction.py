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

from dpp import composite

import pytest
import future.utils
import abc


class Base(future.utils.with_metaclass(abc.ABCMeta, object)):
    def get_int(self):
        pass

    def get_string(self):
        pass


class A(Base):
    def get_int(self):
        return 10

    def get_string(self):
        return 'Hello '


class B(Base):
    def get_int(self):
        return 11

    def get_string(self):
        return 'world!'


@pytest.fixture
def composite_abstract_items():
    a = A()
    b = B()
    return a, b


class TestCompositeReduction:
    def test_reduction(self, composite_abstract_items):

        class Multiplier(object):
            def __init__(self):
                self.value=1

            def __call__(self, value):
                self.value *= value
                return self.value

        class Adder(object):
            def __init__(self):
                self.value = ''

            def __call__(self, value):
                self.value += value
                return self.value

        adder, multiplier = Adder(), Multiplier()

        @composite(interface=Base, reductions={'get_int': multiplier, 'get_string': adder})
        class CompositeFromAbcInterface(object):
            pass

        assert isinstance(CompositeFromAbcInterface, abc.ABCMeta)

        composite_object = CompositeFromAbcInterface()
        composite_object.extend(composite_abstract_items)

        assert composite_object.get_int() == 110
        assert composite_object.get_string() == 'Hello world!'

    def test_wrong_reduction_type(self):
        with pytest.raises(TypeError):
            @composite(interface=Base, reductions=[])
            class CompositeFromAbcInterface(object):
                pass
